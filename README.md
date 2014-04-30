#CMYKsoup#

The Python client for interacting with the CMYKsoup API hosted at api.cmyksoup.com

## class Package ##
Contains the CRUD methods for dealing with package objects. A package contains the products you want to ship. 

###Create a Package ###
For creating a Package, we are providing the following static methods ( You have to call them as Package.method() )

`Package.create(products, customer_id=None, next=None)`
This function expects products to be an array of tuples where each tuple has the product id and the number of items of the product to be packed inside the package. Eg: products=[ ("productid1", 2), ("productid2", 1) ]. 


