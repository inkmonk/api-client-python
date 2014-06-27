#StickyStamp#

The Python client for interacting with the StickyStamp API hosted at api.stickystamp.com

## Installation ##
Download the zip file. Inside the folder named stickystamp, there is a file called default_config.py. Change its name to config.py and set the values of `API_KEY` and `API_SECRET_ACCESS_KEY` with the keys you obtained from us. 
Now run the setup.py with `python setup.py install`. 

-----------------------------------------------------------------------------

## Usage ##
In your python code or the interpreter, just add this import line

`from stickystamp import Merchandise, SKU, Recipient, Shipment, Grant`

-----------------------------------------------------------------------------------------------------------


## SKU ##

A SKU is a stock keeping unit. Each instance of SKU (denoted henceforth as sku in lowercase ) has a unique set of parameters. You Merchandise might have multiple skus.
For exampe, "Contest1 Tshirt" might be a merchandise you had created. It could have several SKUS in it based on color and size like 
'Red L', 'Red XL' , 'Blue M', 'Blue XL'. Each SKU is identified by a unique id

### Attributes ###

`id` - The id of the sku object

`category` - The category of the sku. It can be 'tshirt_merchandise' or 'sticker_merchandise' or 'sticker_sheet_merchandise' or 'postcard_merchandise' or just 'sku' ( in case the sku doesn't belong to any merchandise)

`name` - A name for the SKU. This is usually set only if the sku doesn't belong to any merchandise

`merchandise_name` - The name of the merchandise to which the SKU belongs

`merchandise_id` - The id of the merchandise to which the SKU belongs

The following attributes are set only if the merchandise category is `tshirt_merchandise`

`color` - Tshirt color

`size` - Tshirt size ( 'S', 'M' etc)

`tshirt_type` - Tshirt type ( 'Cotton Roundneck', 'Polycotton Roundneck' etc)

The following attributes are set only if the merchandise category is `sticker_merchandise` or `sticker_sheet_merchandise`

`translucent` - Set to True if the sticker or sticker sheet is translucent

The following attributes are set only if the merchandise category is `sticker_merchandise` or `sticker_sheet_merchandise` or `postcard_merchandise`:

`dimension` - Dimension of the sticker/sheet/card

`dimension_unit` -  The unit in which the dimension is expressed. Default is inch


####Getting all skus####

	SKU.all()

##### Response #####

A list of `SKU` objects

#####Example usage:#####
	
	skus = SKU.all()
	for sku in skus:
		print sku.id, sku.category

####Getting a specific sku####

	SKU.get(id)

##### Response #####

A `SKU` object with the given id

#####Example usage:#####
	
	print SKU.get(1).category


-----------------------------------------------------------------------------------------------------------

## Merchandise ##

The designs you upload become a merchandise. A merchandise might have many skus in it with varying properties. Eg, 'FIFA 2014 Tshirt' is a merchandise. 'FIFA 2014 Tshirt - Red XL', 'FIFA 2014 Tshirt - Blue M' are skus belonging to that merchandise. 

### Attributes ###

`id` - The id of the merchandise

`name` - A unique name for the merchandise ( unique for a given user )

`category` - The category of the merchandise. It can be 'tshirt' or 'sticker' or 'sticker_sheet' or 'postcard'


The following attributes are set only if the merchandise category is `tshirt`

`color` - Tshirt color

`tshirt_type` - Tshirt type ( 'Cotton Roundneck', 'Polycotton Roundneck' etc)


The following attributes are set only if the merchandise category is `sticker` or `sticker_sheet` or `postcard`:

`dimension` - Dimension of the sticker/sheet/card

`dimension_unit` -  The unit in which the dimension is expressed. Default is inch

####Getting all merchandise####

	Merchandise.all()

##### Response #####

A list of `Merchandise` objects

#####Example usage:#####
	
	merchs = Merchandise.all()
	for merch in merchs:
		print merch.id, merch.category, merch.name

####Getting a specific merchandise####

	Merchandise.get(id)

##### Response #####

A `Merchandise` object with the given id

#####Example usage:#####
	
	print Merchandise.get(1).category

----------------------------------------------------------------------------------------------------------------------------


#### Creating a product ####

Use this static method for creating a product

`Product.create(name=None,  third_party=False, template_id=None )`


##### Parameters #####

`name` -  A name for the product. If provided, it has to be unique among all your products. That is you cannot give the same name to any two of your products.

`third_party` - Set this flag to true if the product is manufactured by a third party and CMYKsoup is just used for shipping

`template_id` - Set the template_id of the template to be used (if known)

Note that creating a product does not mean it is ready for shipping. You still need to stock the items of the product by giving us a stock order on our website or offline.


##### Response #####
A `Product` object is returned with all the attributes set.

#####Example usage:#####

`product = Product.create("My Sticker", third_party=True)`

-----------------------------------------------------------------------------

####List all Products####

A list of all product objects belonging to the user with all attributes set

`Product.all()`

-----------------------------------------------------------------------------

####Fetch a product when some attributes are known####

If any of the attributes of the product are known, you can use these methods to fetch the product object. For all these methods `params` denotes keywords arguments where keywords can be anything mentioned in the list of attributes above.



`Product.fetch(*params)` - Returns a list of products matching the attributes provided

#####Example#####
`products=Product.fetch(third_party=True)`

----------------------------------------------

`Product.fetch_one(*params)` - Use this if you want to make sure that exactly one product matches the given attributes.
It will return None if multiple products match or if none match. It will give a product object only if exactly one matches

#####Example#####
`product=Product.fetch_one(name="Contest shirt")`

----------------------------------------------

`Product.get_id(name, *params)` - Use this to get the id of the product if the name or other attributes are known. 

#####Example#####
`product_id=Product.get_id("Contest shirt")`




----------------------------------------------------------------------------------------------------------------------

##Customer##

###Attributes###

`id` - The id of the customer used in our DB
'
And the following self explanatory attributes:

`'name', 'phone_number', 'address1', 'address2','city','state','country','pincode' `

------------------------------------------------------------------------------------

##Package ##

### Attributes ###

`id` - The id of the package used in our DB

`contents` - A list of tuples containing the names and quantities of the products in the package 

`delivery_date` - Promised delivery date

`status` - status of the package

`gross_amount` - Total cost for sending the package including shipping and tax 

`tracking_url` -  The package tracking url

`customer_form_url` - If customer has not been added for the package yet, this is set to an one time form url which can be given to your users 

`customer` - If customer is set, this points to a `Customer` object with various attributes set

-----------------------------------------------------------------------------------------


### Creating a Package ###
For the most common use cases, we have 4 convenience factory methods for creating products.


#### To create a single package of a single product ####

`Package.product( product_name,quantity).create(customer_id, next)`

#####Parameters#####

`customer_id` - Provide the customer id if known. If not provided, the package object returned has the attribute `customer_form_url` set

`next` - Provide the url to redirect the user to, after filling the customer form. If given, the `customer_form_url` attribute will have this value appended at the end as a GET parameter 



#####Returns#####
A package object with various attributes set

#####Example

`package = Package.product( "External Tshirt L",1).create( next= "hackerearth.com" )`

------------------------------------------------------------------------------------------------------

#### To create multiple packages of a single product ####

`Package.product( product_name,quantity).bulk_create(no_of_packages, customer_ids, next)`

#####Parameters#####

`no_of_packages` - The number of packages to create. Provide this if the list of customer ids is not known

`customer_id` - If the list of customers to send is known in advance, provide the list of ids instead of setting the previous parameter

`next` - Provide the url to redirect the user to, after filling the customer form. If given, the `customer_form_url` attribute will have this value appended at the end as a GET parameter


#####Returns#####

A tuple of packages and failures. First is an array of package objects which were created successfully. Second is a list of dictionaries where each has an error message with the key `message` saying why package creation failed for that package

#####Example##### 

`pkgs, failures = Package.product( "External Tshirt L",1).bulk_create(2)`

-------------------------------------------------------------------------------------------------------


#### To create a single package of a set of products ####

`Package.products( *args ).create(customer_id, next)`

#####Parameters#####

`*args` - Each arg is a tuple containing the product name and quantity. Any number of tuples can be given

`customer_id` - Provide the customer id if known. If not provided, the package object returned has the attribute `customer_form_url` set

`next` - Provide the url to redirect the user to, after filling the customer form. If given, the `customer_form_url` attribute will have this value appended at the end as a GET parameter 


#####Returns#####

A package object with various attributes set

#####Example#####

`pkg = Package.products( ("Globe Tshirt L",1), ("New Tshirt M",1) ).create( next= "hackerearth.com" )`

-----------------------------------------------------------------------------------------------------

#### To create multiple packages of a set of products ####

`Package.products( * args ).bulk_create(no_of_packages, customer_ids, next)`


#####Parameters#####

`*args` - Each arg is a tuple containing the product name and quantity. Any number of tuples can be given

`no_of_packages` - The number of packages to create. Provide this if the list of customer ids is not known

`customer_id` - If the list of customers to send is known in advance, provide the list of ids instead of setting the previous parameter

`next` - Provide the url to redirect the user to, after filling the customer form. If given, the `customer_form_url` attribute will have this value appended at the end as a GET parameter


#####Returns#####

A tuple of packages and failures. First is an array of package objects which were created successfully. Second is a list of dictionaries where each has an error message with the key `message` saying why package creation failed for that package

#####Example#####
`pkgs, failures = Package.products( ("Globe Tshirt L",1), ("New Tshirt M",1) ).bulk_create(2)`

-----------------------------------------------------------------------------------------------------

#### Listing all packages ####

`Package.all()`

#####Returns#####

A list of package objects

-------------------------------------------------------------------------------------------------------

####Fetching the details of a package ####

`Package.get(id)`

#####Returns#####

A package object with all attributes set. If no matching id was found in DB, it returns None










