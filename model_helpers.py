import hmac
from hashlib import sha1
from decimal import Decimal

class Serializer(object):
    """SQLAlchemy Model JSON Serializer

    A class to help serialize sqlalchemy models
    in JSON format
    """
    __public__ = None

    def to_serializable_dict(self):
        data = {}
        for key in self.__table__.columns.keys():
            data[key] = getattr(self, key)

        for key in self.__mapper__.relationships.keys():
            if key in self.__public__:
                if self.__mapper__.relationships[key].uselist:
                    data[key] = []
                    for item in getattr(self, key):
                        data[key].append(item.to_dict())
                else:
                    data[key] = getattr(self, key)

        return data

def monetize(number):
  return Decimal(number).quantize(Decimal('.01'))

