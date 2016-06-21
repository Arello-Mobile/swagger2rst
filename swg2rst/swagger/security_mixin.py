class SecurityMixin(object):

    security = None

    def _fill_securities(self, obj):
        if obj.get('security'):
            self.security = {}
            for security in obj['security']:
                self.security.update(security)
