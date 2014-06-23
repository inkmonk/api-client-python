import json, requests, hmac, decimal, config
from hashlib import sha1


class Serializer(object):
    """SQLAlchemy Model JSON Serializer

    A class to help serialize sqlalchemy models
    in JSON format
    """
    __public__ = None

    def to_serializable_dict(self):
        data = {}
        for key in self.__table__.columns.keys():
            value = getattr(self, key)
            if type(value) is decimal.Decimal:
                data[key] = "%.2f" % round(float(value), 2)
            else:
                data[key] = value

        for key in self.__mapper__.relationships.keys():
            if key in self.__public__:
                if self.__mapper__.relationships[key].uselist:
                    data[key] = []
                    for item in getattr(self, key):
                        data[key].append(item.to_serializable_dict())
                else:
                    data[key] = getattr(self, key)

        return data


def get_signature(secret_key, request=None, message=None):
    """Generate signature

    Method to sign a http request using HMAC
    """
    if request:
        message = request.path + request.method + request.headers['Content-Type']
    signature = hmac.new(secret_key, message, sha1)
    return signature.hexdigest()


def send_request(method, path, payload=None):
    #print "sending request to %s with payload %s" % (path, str(payload))
    url = config.API_BASE_URL + path
    message = path + method + "application/json"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "%s:%s" % (config.API_KEY,
                                    get_signature(str(config.API_SECRET_ACCESS_KEY),
                                                  message=message))
    }
    if method=="POST":
      res = requests.post(url, data=json.dumps(payload), headers=headers)
    elif method=="GET":
      if payload:
        res = requests.get(url, headers=headers, params=payload )
      else:
        res = requests.get(url, headers=headers )
    elif method=="PUT":
      res = requests.put(url, data=json.dumps(payload), headers=headers)
    elif method=="DELETE":
      res = requests.delete(url, headers=headers)
    else:
      res=None
    return res

def _filter_params(params, whitelist):
    return dict([(k,v) for k,v in params.iteritems() if k in whitelist ])

def ping():
    return send_request('GET','/').json()


class Customer:

    def __init__(self, **kwargs):
        for k,v in _filter_params(kwargs, ('id','name', 'phone_number', 'address1', 'address2','city','state','country','pincode')).iteritems():
            setattr(self, k, v)


class Package:

    def __init__(self, **kwargs):
        for k,v in _filter_params(kwargs, ('id','contents','status', 'gross_amount', 'tracking_url', 'customer_form_url', 'recipient')).iteritems():
            if k is 'customer' and v is not None and isinstance(v,dict):
                setattr(self, k, Customer(**v) )
            setattr(self, k, v)

    @staticmethod
    def create( *args, **kwargs):
        customer_id=None
        if 'customer_id' in kwargs:
            customer_id=kwargs['customer_id']
        products=list(args)
        response = send_request('POST', '/v1/packages', {'products': products, 'customer_id': customer_id })
        if response.status_code in (200,201):
            pkg=response.json()['package']
            if 'next' in kwargs:
                next=kwargs['next']
                if next:
                    if not next.startswith("http://www."):
                        next="http://www."+next
                    pkg['customer_form_url']+='&next=%s' % next
            return Package(**pkg)
        else:
            print response.json()
            return None

    @staticmethod
    def bulk_create(packages, next=None):
        """Create Multiple Orders in one call
        :param packages:
        A list of packages. Each package should be a dict with 2 keys. `customer_id` should be the customer to send the package to. If not known,
        specify it as None. `products` should be a list of tuples,  with first element being the product id, second element should be an integer denoting the quantity.

        Eg: add_multiple_packages( [ { 'products': [ ('4223fere4fds',5),('4w452f23423',3) ], 'customer_id': 'vsdtgweert' },
                                     {'products': [('4w452f23423',5)], 'customer_id': 'xasdgawetfs' } ] )
        """
        response = send_request('POST', '/v1/bulk/packages', {'packages': packages })
        if response.status_code in (200,201):
            packages=[]
            pkgs = response.json()['packages']
            if next:
                if not next.startswith("http://www."):
                    next="http://www."+next
                for pkg in pkgs:
                    if 'customer_form_url' in pkg:
                        pkg['customer_form_url']+='&next=%s' % next
            for pkg in pkgs:
                packages.append(Package(**pkg ))
            return (packages, response.json()['errors'])
        else:
            print response.json()
            return []

    
    class product:

        def __init__(self, product_name, quantity):
            id=Product.get_id(product_name)
            if id is None:
                raise NameError("No product found with name matching %s" % product_name)
            self.product=id
            self.quantity=quantity

        def create(self, customer_id=None, next=None):
            return Package.create( (self.product, self.quantity), customer_id=customer_id, next=next )


        def bulk_create( self,  no_of_packages=1, customer_ids=None, next=None):
            """Convenience method for adding packages in batch where each package has only one product
            :param product:
            The product id for the product to be added in every package
            :param qty_per_package:
            The number of products to add per package
            :param no_of_packages:
            The number of packages to generate
            """
            if customer_ids is None:    
                return Package.bulk_create( [ {'products':[(self.product, self.quantity)], 'customer_id': None } for i in range(no_of_packages) ], next=next )
            else:
                return Package.bulk_create( [ {'products':[(self.product, self.quantity )], 'customer_id': id } for id in customer_ids ], next=next )

    class products:

        def __init__(self, *args):
            self.products=[]
            for p,q in args:
                id=Product.get_id(p)
                if id is None:
                    raise Exception("No product found with name matching %s" % p)
                self.products.append((id,q))


        def create(self, customer_id=None, next=None):
            return Package.create(*self.products, customer_id=customer_id, next=next)

        def bulk_create (self,  no_of_packages=None, customer_ids=None, next=None):
            """Convenience method for adding batch packages
            :param package_contents:
            A list of tuples. First element should be the product id, second element should be an integer denoting the quantity
            :param no_of_packages:
            The number of packages to create. Set this parameter if you are not providing the list of customer customer_ids
            :param customer_ids:
            List of customer ids ( optional )
            """
            if customer_ids is None:
                return Package.bulk_create( [ {'products': self.products, 'customer_id': None } for i in range(no_of_packages) ], next=next )
            else:
                return Package.bulk_create( [ {'products': self.products, 'customer_id': id } for id in customer_ids ] , next=next)

    @staticmethod
    def all():
        response = send_request('GET', '/v1/packages')
        res=response.json()
        if 'packages' in res:
            return [ Package(**pkg) for pkg in res['packages'] ]
        else:
            print res
            return []

    @staticmethod
    def get(id):
        response = send_request('GET', '/v1/packages/%s' %id)
        res=response.json()
        if response.status_code in (200, 201):
            return Package(**res)
        else:
            return None





class Product:

    def __init__(self, **kwargs):
        for k,v in _filter_params(kwargs, ('id','name', 'properties','status', 'quantity', 'third_party')).iteritems():
            setattr(self, k, v)

    @staticmethod
    def create(name, template_code, third_party=False, properties={} ):
        request={'third_party': third_party, 'name': name, 'template_code': template_code, 'properties': properties}
        response = send_request('POST', '/v1/products', request)
        if response.status_code in (200, 201, 302):
            return Product(**_filter_params(response.json(), ('id','name', 'design_id','status', 'quantity', 'third_party') ) )
        else:
            print response.json()
            return None

    @staticmethod
    def all():
        response = send_request('GET', '/v1/products')
        print response
        if 'products' in response.json():
            return [ Product(**_filter_params(product, ('id','name', 'design_file','status', 'quantity', 'third_party'))) for product in response.json()['products'] ]
        else:
            return []

    @staticmethod
    def fetch(**params):
        response = send_request('GET', '/v1/products', params)
        if 'products' in response.json():
            return [ Product(**_filter_params(product, ('id','name', 'design_file','status', 'quantity', 'third_party'))) for product in response.json()['products'] ]
        else:
            return []

    @staticmethod
    def fetch_one(**params):
        params['one']=True
        response = send_request('GET', '/v1/products', params)
        if 'product' in response.json():
            return Product(**_filter_params(response.json()['product'], ('id','name', 'design_file','status', 'quantity', 'third_party'))) 
        else:
            return None

    @staticmethod
    def get_id(name=None, **params):
        if name:
            params['name']=name
        result = Product.fetch_one(**params)
        if isinstance(result, Product):
            return result.id
        else:
            return None

    def __repr__(self):
        return self.name



if __name__ == '__main__':
    pass

