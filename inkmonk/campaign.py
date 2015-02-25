from resource import Resource


class Campaign(Resource):

    _resource_ = 'campaigns'

    def __repr__(self):
        return self.name
