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

This id can be obtained from the site for each merchandise. Or calling `Merchandise.all()` will list all the merchandise names with this id for each merchandise within angular braces.

##### Response #####

A `Merchandise` object with the given id

#####Example usage:#####
	
	print Merchandise.get("PC1-WCRD").category

####Fetching skus belonging to the merchandise####

If no params are supplied, the method returns all the skus belonging to the merchandise. Otherwise if filters based on the params and returns a filtered list of skus.

	merchandise.skus(**params)

##### Response #####

A list of `SKU` objects

#####Example usage:#####
	
	merchandise=Merchandise.get("PC1-WCRD")
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
	
	merchandise=Merchandise.get("T1-CNTS1")
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

	shipment1 = Shipment.create( recipient={ 'name': 'Surya', 'email': 'surya@stickystamp.com', 
											'address1': 'No 12, Krishnan Street', 
											'address2': 'Govindan Road, West Mambalam', 
											'city': 'Chennai', 'state': 'Tamilnadu', 
											'pincode': '600033', 'contact_number': '8888888888' }, 
								contents= [ ('T1-CNTS1-V1-XL',2),
											 ('S1-NEW-V1',1) 
										] )


The SKU strings used in the contents can be obtained from your dashboard. Alternatively, you can just obtain the list of SKUs dynamically as illustrated below

First obtain the merchandise. There are 2 ways of doing this

		merchs=Merchandise.all()
		tshirt=merchs[1]
		sticker=merchs[0]

Or

		tshirt=Merchandise.get("T1-CNTS1")
		sticker=Merchandise.get("S1-CNOS1")

In the second case, you need to provide the merchandise code, which can also be got from the dashboard. After obtaining the merchandise object, you can call create the contents list as follows

	shipment2 = Shipment.create( recipient={ 'name': 'Isaac', 
											'email': 'isaac@stickystamp.com', 
											'address1': 'No 12, Krishnan Street', 
											'address2': 'Govindan Road, West Mambalam', 
											'city': 'Chennai', 'state': 'Tamilnadu', 
											'pincode': '600033', 'contact_number': '8888888888' }, 
								contents= [ (tshirt.sku(color='Red', size='M' ),1), 
											(sticker.sku(translucent=False),1) 
										] )




--------------------------------------------------------------------------------------------------------------------------------


##GrantForm##

A grantform is an url for a one time form that you provide to your customers/recipients and ask them to fill out their shipping address. You can also let them choose between different SKUS. For eg: You can add 10 different SKUs ( Red Medium, Blue Medium, Red Large etc) of the merchandise 'Contest Tshirt1' to a field in the form. You can also specify the quantity of items that can be chosen from that slot. Your customer will then see a field in the form with all these choices allowing him to choose between the variations.  You can also add multiple such fields to the form

### Attributes ###

`id` - The id of the grantform

`token` - a unique string which is passed as a part of the url

`url` - The URL of the form that you need to send to your recipient

`is_valid` - This becomes false if the recipient has filled up the form or if the date of expiry has crossed

`converted` - A boolean which denotes whether the recipient has submitted the details converting the GrantForm into a shipment

`expires_on` - The date on which this form will expire

`mailed_to` - Set this field to remember the email address to which you mailed this form url to

`choices` - A list of tuples. Each tuple has 2 elements. The first element is a list of skus which you want to give as choices for that field. The second element denotes the quantity of skus that you want to let the user choose in that field.

`shipment` - A shipment object. This gets set when the recipient fills up the details and submits the form. This shipment object contains all the details submitted by the recipient



####Getting all grantforms####

	GrantForm.all()

##### Response #####

A list of `GrantForm` objects

#####Example usage:#####
	
	for grantform in GrantForm.all():
		print grantform.url
		if grantform.converted:
			print grantform.shipment.id, grantform.shipment.recipient, grantform.shipment.contents
		else:
			for skus,quantity in grantform.choices:
				print quantity
				for sku in skus:
					print sku.id

####Getting a specific grantform####

	GrantForm.get(id)

##### Response #####

A `GrantForm` object with the given id

#####Example usage:#####

	grantform = GrantForm.get(1)
	if grantform.converted:
		print grantform.shipment.id, grantform.shipment.recipient, grantform.shipment.contents
	else:
		for skus,quantity in grantform.choices:
			print quantity
			for sku in skus:
				print sku.id

####Creating a grantform####

	GrantForm.create(choices, days_till_expiry=90, mailed_to=None)

The arg `choices` expects a list of tuples. The first element should be a list of skus. The list can either be made of sku objects or sku id strings. The second element should be the number of items the recipient can be allowed to choose from the list.

The arg `days_till_expiry` is used to set the validity of the form. By default it is 90 days.

The arg `mailed_to` is used to set the mail address to which you will mail the form url to. 


##### Response #####

A `GrantForm` object

#####Example usage:#####

	grantform = GrantForm.create( choices=[ ( ['T1-CNTS1-V1-XL','T1-CNTS1-V1-L','T1-CNTS1-V1-M', 'T1-CNTS1-V1-S'], 2), 
											(  ['S1-NEW-V1','S1-NEW-V2-T'], 1) 
										] )

The SKU strings used to populate each individual tuple of the choices can be obtained from your dashboard. Alternatively, you can just obtain the list of SKUs dynamically as illustrated below

First obtain the merchandise. There are 2 ways of doing this

		merchs=Merchandise.all()
		tshirt=merchs[1]
		sticker=merchs[0]

Or

		tshirt=Merchandise.get("T1-CNTS1")
		sticker=Merchandise.get("S1-CNOS1")

In the second case, you need to provide the merchandise code, which can also be got from the dashboard. After obtaining the merchandise object, you can call create the choices list as follows

		form=GrantForm.create( choices=[ (tshirt.skus(),2), 
										(sticker.skus(),1) 
										], 
								mailed_to="surya@stickystamp.com", 
								)

You can also filter the choices of the SKUs. For example, if you want the user to be able to choose only between red tshirts, you can do this

		form=GrantForm.create( choices=[ (tshirt.skus( color="red"), 2 ), 
										(sticker.skus(),1) 
										], 
								mailed_to="surya@stickystamp.com", 
								days_till_expiry=30 )

You might also want to give the choice to user only for some merchandise and pre-determine the other merchandise ( Eg: Always send a 3x3 sticker, but let the user choose the color and size of tshirt ). In that case, the tuples given as a part of the choices list, should have just a single element list as a first item. 

For eg, in the below example, while all skus of tshirts are being given as choices, the sticker is limited to just one SKU. 


		form=GrantForm.create( choices=[ (tshirt.skus(), 2 ), 
										([ SKU.get('S1-NEW-V1') ],1) 
										], 
								mailed_to="surya@stickystamp.com", 
								days_till_expiry=30 )

Even in the above example, it is not necessary for you to know the SKU of the particular item you want to choose. You can use it as below instead

		form=GrantForm.create( choices=[ (tshirt.skus(), 2 ), 
										([ merchs[0].sku(translucent=False) ],1) 
										], 
								mailed_to="surya@stickystamp.com", 
								days_till_expiry=30 )


You can obtain the url from the form by accessing `form.url`



