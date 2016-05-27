from .abstractTypeObject import AbstractTypeObject
from .constants import PRIMITIVE_TYPES, SchemaTypes
from .header import Header


class Response(AbstractTypeObject):
    """ Represents Swagger Response Object
    """
    headers = None
    examples = None

    def __init__(self, obj, **kwargs):
        super(Response, self).__init__(obj, **kwargs)
        self.description = obj.get('description')
        self.examples = obj.get('examples')

        if 'schema' in obj:
            self._set_type()

        if 'headers' in obj:
            self.headers = {name: Header(header, name=name, root=self.root)
                            for name, header in obj['headers'].items()}

    def _set_type(self):
        if 'type' in self.raw['schema'] and self.raw['schema']['type'] in PRIMITIVE_TYPES:
            self._type = self.raw['schema']['type']
            self.type_format = self.raw['schema'].get('format')
            _, _, self.properties = self.get_type_properties(self.raw, self.name)
        else:
            self.set_type_by_schema(self.raw['schema'], SchemaTypes.INLINE)
