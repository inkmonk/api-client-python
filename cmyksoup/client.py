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


class Package:

    def __init__(self, id):
        details = Package.get(id)
        if details['status']==404:
            raise NameError("No package found with id %s" % id )
        for k,v in details.iteritems():
            setattr(self, k, v)

    @staticmethod
    def create( *args, **kwargs):
        """Create a package

        :param products:
        A list of tuples. First element should be the product id, second element should be an integer denoting the quantity

        :param customer_id:
        An optional argument denoting the customer id to associate the package with. If this is not provided, the response json will contain
        an url pointing to a form for creating a customer entry
        """
        customer_id=None
        if 'customer_id' in kwargs:
            customer_id=kwargs['customer_id']
        products=list(args)
        response = send_request('POST', '/v1/packages', {'products': products, 'customer_id': customer_id })
        result=response.json()
        print result
        if 'next' in kwargs:
            next=kwargs['next']
            if next:
                if not next.startswith("http://www."):
                    next="http://www."+next
                result['url']+='&next=%s' % next
        return result

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
        results = response.json()
        if next:
            if not next.startswith("http://www."):
                next="http://www."+next
            for result in results:
                if 'url' in result:
                    result['url']+='&next=%s' % next
        

        return results

    
    class of_product:

        def __init__(self, product_name, quantity):
            id=Product.id(product_name)
            if id is None:
                raise NameError("No product found with name matching %s" % product_name)
            self.product=Product.id(product_name)
            self.quantity=quantity

        def create(self, customer_id=None, next=None):
            products=[(self.product, self.quantity)]
            response = send_request('POST', '/v1/packages', {'products': products, 'customer_id': customer_id })
            result=response.json()
            if next:
                if not next.startswith("http://www."):
                    next="http://www."+next
                result['url']+='&next=%s' % next
            return result

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

    class of_products:

        def __init__(self, *args):
            self.products=[]
            for p,q in args:
                id=Product.id(p)
                if id is None:
                    raise Exception("No product found with name matching %s" % p)
                self.products.append((id,q))


        def create(self, customer_id=None, next=None):
            return Package.create(products= self.products, customer_id=customer_id, next=next)

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
        if 'products' in response.json():
            return response.json()
        else:
            return response.json()

    @staticmethod
    def get(id):
        response = send_request('GET', '/v1/packages/%s' %id)
        return response.json()

    @staticmethod
    def edit(id, payload):
        response = send_request('PUT', '/v1/packages/%s' % id, payload)
        return response.json()



class Product:

    @staticmethod
    def create(name=None,  third_party=False, template_id=None ):
        request={'third_party': third_party}
        if name:
            request['name']=name
        if template_id:
            request['template_id']=template_id
        response = send_request('POST', '/v1/products', request)
        result=_filter_params(response.json(), ('id','name', 'design_file','status', 'quantity', 'third_party') )
        return result

    @staticmethod
    def all():
        response = send_request('GET', '/v1/products')
        if 'products' in response.json():
            return [ _filter_params(product, ('id','name', 'design_file','status', 'quantity', 'third_party')) for product in response.json()['products'] ]
        else:
            return response.json()

    @staticmethod
    def fetch(**params):
        response = send_request('GET', '/v1/products', params)
        if 'products' in response.json():
            return [ _filter_params(product, ('id','name', 'design_file','status', 'quantity', 'third_party')) for product in response.json()['products'] ]
        else:
            return response.json()

    @staticmethod
    def fetch_one(**params):
        params['one']=True
        response = send_request('GET', '/v1/products', params)
        if 'products' in response.json():
            return [ _filter_params(product, ('id','name', 'design_file','status', 'quantity', 'third_party')) for product in response.json()['products'] ]
        else:
            return response.json()

    @staticmethod
    def id(name=None, **params):
        if name:
            params['name']=name
        result = Product.fetch_one(**params)
        if 'id' not in result:
            return None
        return result['id']



if __name__ == '__main__':
    #products = [ product for product in get_products() if product['quantity'] > 0 ]
    #products = [ (product['id'], product['name'] )for product in get_products() ]
    print Product.create("My 3rd party tshirt1", third_party=True )
    #print products
    #response= add_package( [ (products[0]['id'],1), (products[1]['id'], 2) ] )
    #print len(response[])
    #print add_multiple_packages( [ { 'products': [ (products[0]['id'],1),(products[1]['id'],1) ], 'customer_id': None },
                                 #{'products': [(products[1]['id'],3)], 'customer_id': None } ] )

    #print batch_package(products[1]['id'],2,4)

