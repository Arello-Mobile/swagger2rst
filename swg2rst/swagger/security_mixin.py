class SecurityMixin(object):

    security = None

    def _fill_securities(self, obj):
        self.security = {}
        for security in obj:
            self.security.update(security)
