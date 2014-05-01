#CMYKsoup#

The Python client for interacting with the CMYKsoup API hosted at api.cmyksoup.com

## class Package ##
Contains the CRUD methods for dealing with package objects. A package contains the products you want to ship. 

###Create a Package ###
For creating a Package, we are providing the following static methods ( You have to call them as Package.method() )

####`Package.create(*args, **kwargs)` ####

##### Parameters #####

`args` - Each arg is a tuple of the product id and the number of items of the product to be packed inside the package. 
Eg: `Package.create( (Product.get("Tshirt L"), 2), (Product.get("Sticker1"), 1) ) ` 
######Permitted kwargs:######
`customer_id` - The id of the customer to whom the package should be shipped. Default is None. If left as None, the response object would contain an url to an one time customer creation form which you can give to your customers for filling the details themselves.
`next` - The url to which you want to redirect the customer to , after successfully submitting the details in our form.  

##### Response #####
The response is a json object with the status of the operation, the id of the created package and an one time customer creation url (if customer id was not given ). 
Example Response: `{u'status': u'success', u'url': u'http://www.cmyksoup.com/customers/new?token=06ccd112fc9c49f3a3f586bf4e060b27&next=http://www.www.hackerearth.com', u'id': u'875bace3ad4d4e1690244048752459e7'}`




