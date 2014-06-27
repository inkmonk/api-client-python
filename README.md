#StickyStamp#

The Python client for interacting with the StickyStamp API hosted at api.stickystamp.com

## Installation ##
Download the zip file. Inside the folder named stickystamp, there is a file called default_config.py. Change its name to config.py and set the values of `API_KEY` and `API_SECRET_ACCESS_KEY` with the keys you obtained from us. 
Now run the setup.py with `python setup.py install`. 

-----------------------------------------------------------------------------

## Usage ##
In your python code or the interpreter, just add this import line

`from stickystamp import Merchandise, SKU, Recipient, Shipment, Grant`

Use the factory methods documented below for interacting with the objects. Each method call is actually a request to Stickystamp API. Do not instantiate the objects yourself. The objects will have the relevant data only if instantiated using the factory methods. 

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

####Fetching skus belonging to the merchandise####

If no params are supplied, the method returns all the skus belonging to the merchandise. Otherwise if filters based on the params and returns a filtered list of skus.

	merchandise.skus(**params)

##### Response #####

A list of `SKU` objects

#####Example usage:#####
	
	merchandise=Merchandise.get(2)
	print "Printing all skus belonging to merchandise 2"
	for sku in merchandise.skus():
		print sku.id
	print "Printing the skus belonging to merchandise 2 which are Red in color"
	for sku in merchandise.skus(color='Red'):
		print sku.id

####Fetching exacting one sku belonging to the merchandise####

Use this method if you want to ensure that exactly one sku object matches the filter params. If there is no match or if there is more than one match, this method returns None.

	merchandise.sku(**params)

##### Response #####

A `SKU` object

#####Example usage:#####
	
	merchandise=Merchandise.get(2)
	sku = merchandise.sku(color='Red', size='M')
	print sku.id

--------------------------------------------------------------------------------------------------------------------------------

## Recipient ##

A recipient is a recipient address to which you send your shipments to.

### Attributes ###

`id` - The id of the recipient
`name` - The name of the recipient
`email` - The email address of the recipient
`address1` -  First line of address ( Door no, street)
`address2` - Second line of address
`city` - City of residence of the recipient
`state` - State of residence of the recipient
`country` - Country of residence of the recipient
`pincode` - Pincode or Zipcode
`contact_number` - Contact number of the recipient



--------------------------------------------------------------------------------------------------------------------------------


## Shipment ##

A shipment is the package that you ship to a recipient. It has a recipient ( Name, email and address ) and some contents ( A set of skus )

### Attributes ###

`id` - The id of the shipment

`recipient` - A recipient object with the attributes set

`status` - Status of the shipment

`tracking_url` - The courier tracking url of the shipment

`shipping_charges` - Charges levied for shipping

`net_amount` - Shipping charges + packing cost

`tax` - Tax amount

`gross_amount` - Total bill for the shipment

`contents` - A list of tuples. Each tuple has two elements. First element is a sku object. The second element is the quantity of that sku present in the shipment.


####Getting all shipments####

	Shipment.all()

##### Response #####

A list of `Shipment` objects

#####Example usage:#####
	
	for shipment in Shipment.all():
		print shipment.recipient.name
		for sku,quantity in shipment.contents:
			print sku.id, sku.merchandise_name, quantity

####Getting a specific shipment####

	Shipment.get(id)

##### Response #####

A `Shipment` object with the given id

#####Example usage:#####

	for sku,quantity in Shipment.get(1).contents:
		print sku.id, sku.merchandise_name, quantity

####Creating a shipment####

	Shipment.create(recipient, contents)

The arg `recipient` expects a dictionary with keys as the attributes of `Recipient` ie `name`, `email`, `address1` etc

The arg `contents` expects a list of tuples. The first element of tuple can either be a sku object or the id of a sku object. The second element is the quantity of that sku to be added to the shipment

##### Response #####

A `Shipment` object

#####Example usage:#####

	shipment1 = Shipment.create( recipient={ 'name': 'Surya', 'email': 'surya@stickystamp.com', 'address1': 'No 12, Krishnan Street', 'address2': 'Govindan Road, West Mambalam', 'city': 'Chennai', 'state': 'Tamilnadu', 'pincode': '600033', 'contact_number': '8888888888' }, contents= [ ('M1V1',2), ('M2V2',1) ] )

	shipment2 = Shipment.create( recipient={ 'name': 'Isaac', 'email': 'isaac@stickystamp.com', 'address1': 'No 12, Krishnan Street', 'address2': 'Govindan Road, West Mambalam', 'city': 'Chennai', 'state': 'Tamilnadu', 'pincode': '600033', 'contact_number': '8888888888' }, contents= [ (Merchandise.get(1).sku(color='Red', size='M' ),1), ('M2V2',1) ] )

	
