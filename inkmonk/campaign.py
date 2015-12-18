from resource import Resource


class Campaign(Resource):

    _resource_ = 'campaigns'

    def __init__(self, **kwargs):
        super(Campaign, self).__init__(**kwargs)
        self.Claim._resource_ = 'campaigns/%s/claims' % self.id

    def __repr__(self):
        return self.name

    class Claim(Resource):
        _resource_ = None