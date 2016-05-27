from swg2rst.converter_exceptions import ConverterError
from .abstractTypeObject import AbstractTypeObject
from .constants import SchemaTypes


class Parameter(AbstractTypeObject):
    """ Represents Swagger Parameter Object
    """
    def __init__(self, obj, **kwargs):
        super(Parameter, self).__init__(obj, **kwargs)
        self.location_in = obj['in']
        self.required = obj.get('required', False)
        self.description = obj.get('description', '')
        self.default = obj.get('default')
        self.collection_format = obj.get('collectionFormat')

        self._set_type()

    def _set_type(self):
        if 'type' in self.raw:
            self._type = self.raw['type']
            self.type_format = self.raw.get('format')
            if self.is_array:
                self.item = dict(zip(
                    ('type', 'type_format', 'type_properties'),
                    self.get_type_properties(self.raw['items'], self.name)))
            else:
                _, _, self.properties = self.get_type_properties(self.raw, self.name)
        elif 'schema' in self.raw:
            self.set_type_by_schema(self.raw['schema'], SchemaTypes.INLINE)
        else:
            raise ConverterError('Invalid structure')

    @property
    def type(self):
        if self.is_array:
            return 'array of {}'.format(self.item['type'])
        else:
            return self._type

    def __repr__(self):
        return '{}_{}'.format(self.location_in, self.name)
