class SecurityDefinition(object):
    '''
    Represents Swagger Security Scheme Object
    '''
    scopes = None
    location_in = None
    param_name = None
    flow = None
    auth_url = None
    token_url = None

    def __init__(self, name, obj):

        self.name = name
        self.type = obj['type']
        assert self.type in SecurityTypes.names

        self.description = obj.get('description', '')
        self.raw = obj

        if self.type == SecurityTypes.API_KEY:
            self.location_in = obj['in']
            self.param_name = obj['name']
        elif self.type == SecurityTypes.OAUTH2:
            self.flow = obj['flow']
            assert self.flow in ('implicit', 'password', 'application', 'accessCode')

            if self.flow in ('implicit', 'accessCode'):
                self.auth_url = obj['authorizationUrl']
            if self.flow in ('password', 'accessCode', 'application'):
                self.token_url = obj['tokenUrl']

            self.scopes = obj['scopes']

    @property
    def type_name(self):
        return SecurityTypes.names[self.type]
