#CMYKsoup#

The Python client for interacting with the CMYKsoup API hosted at api.cmyksoup.com

## Installation ##
Download the zip file. Inside the folder named cmyksoup, there is a file called default_config.py. Change its name to config.py and set the values of `API_KEY` and `API_SECRET_ACCESS_KEY` with the keys you obtained from us. 
Now run the setup.py with `python setup.py install`. 

## Usage ##
In your python code or the interpreter, just add this import line
`from cmyksoup import *`
That's all. You are good to go.

## class Product ##
contains the CRUD methods for dealing with product objects. A product is what you create after choosing our template and uploading a design file. 

####`Product.create(name=None,  third_party=False, template_id=None )` ####
A static method for creating a product.
##### Parameters #####
`name` -  A name for the product. If provided, it has to be unique among all your products. That is you cannot give the same name to any two of your products.
`third_party` - Set this flag to true if the product is manufactured by a third party and CMYKsoup is just used for shipping
`template_id` - Set the template_id of the template to be used (if known)
Note that creating a product does not mean it is ready for shipping. You still need to stock the items of the product by giving us a stock order on our website or offline.
Example usage:
`Product.create("My Sticker", third_party=True)`

##### Response #####
A dictionary of properties and values of the created product
Example response:
`{u'status': u'pending_with_moderator', u'third_party': True, u'name': u'My Sticker 2', u'design_file': None, u'id': u'f13e1c9609d943d1b94df57edec82187', u'quantity': 0}`


## class Package ##
Contains the CRUD methods for dealing with package objects. A package contains the products you want to ship. 

###Get a Package's id ###
####`Package.create(*args, **kwargs)` ####
You need the Package's id number for most operations. This method lets

###Create a Package ###
For creating a Package, we are providing the following static methods ( You have to call them as Package.method() )

####`Package.create(*args, **kwargs)` ####

##### Parameters #####

`args` - Each arg is a tuple of the product id and the number of items of the product to be packed inside the package. 
Eg: `Package.create( (Product.id("Tshirt L"), 2), (Product.id("Sticker1"), 1) ) ` 
######Permitted kwargs:######
`customer_id` - The id of the customer to whom the package should be shipped. Default is None. If left as None, the response object would contain an url to an one time customer creation form which you can give to your customers for filling the details themselves.
`next` - The url to which you want to redirect the customer to , after successfully submitting the details in our form.  

##### Response #####
The response is a json object with the status of the operation, the id of the created package and an one time customer creation url (if customer id was not given ). 
Example Response: `{u'status': u'success', u'url': u'http://www.cmyksoup.com/customers/new?token=06ccd112fc9c49f3a3f586bf4e060b27&next=http://www.www.hackerearth.com', u'id': u'875bace3ad4d4e1690244048752459e7'}`




