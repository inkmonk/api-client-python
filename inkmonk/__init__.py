import core
import config
from merchandise import Merchandise, Tshirt
from customer import Customer
from shipment import Shipment
from sku import SKU
from claim import Claim
from campaign import Campaign


def configure(key=None, secret=None):
    config.API_KEY = key
    config.API_SECRET = secret
