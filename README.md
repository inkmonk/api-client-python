#Inkmonk - python client#

The Python client for interacting with the Inkmonk API hosted at https://inkmonk.in/api/v1

## Installation ##

1. Download the zip file. 
2. Run  `python setup.py install`. 
3. Set api key and secret key as follows, 

		import inkmonk
		inkmonk.config.API_KEY='4f52176c7b894a9ab5a15777feeba02124022015190803287306'
		inkmonk.config.API_SECRET='a63421f75f9b4bb58fb3ae63fffbfd9024022015190803287405'

4. Start using

		inkmonk.Merchandise.all()

Alternatively you can also set the API KEY and API_SECRET in the config.py file itself after step 1 and do only step 2. You can then start using it without having to set programmatically.

-----------------------------------------------------------------------------

## Usage ##

The following classes are available

1. Merchandise
2. SKU
3. Tshirt
4. Claim
5. Campaign
6. Shipment

For all these classes you have the following methods available

1. create

		c=Campaign.create(
			slots=[{'quantity': 1,
					'choices': [sk.id for sk in sks]}],
			campaign_title="This is a new campaign",
			customers=['surya@stickystamp.com'],
			template_body="Hello",
			template_header="Heading",
			form_title="Awesome Title")

2. all

		tshirts = inkmonk.Tshirt.all()

		for t in tshirts:
			print t.name

3. get
	
		tee = inkmonk.Tshirt.get('U1-C81C-TS-RNE-CO')

4. update
	
		tee_updated = inkmonk.Tshirt.update('U1-C81C-TS-RNE-CO', color="Navy Blue")

5. patch

Apart from these methods, you can also directly use the core HTTP methods on specific endpoints
if the structure is non standard REST ( for internal use )
The following core methods are present

1. get
2. all
3. post
4. put
5. patch

Eg: 

	inkmonk.core.all('skus', {'categorized': 'old'})