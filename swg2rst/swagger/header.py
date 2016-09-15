from swg2rst.converter_exceptions import ConverterError
from .abstract_type_object import AbstractTypeObject
from .constants import PRIMITIVE_TYPES


class Header(AbstractTypeObject):
    """
    Represents Swagger Header Object
    """

    def __init__(self, obj, **kwargs):
        super(Header, self).__init__(obj, **kwargs)
        self.description = obj.get('description')
        self._set_type()

    def _set_type(self):
        self._type = self.raw['type']
        if self._type not in PRIMITIVE_TYPES and self._type != 'array':
            raise ConverterError(
                'Invalid type of response header {}'.format(self.name))

        self.type_format = self.raw.get('format')
        if self.is_array:
            self.item = dict(zip(
                ('type', 'type_format', 'type_properties'),
                self.get_type_properties(self.raw['items'], self.name)))
        else:
            _, _, self.properties = self.get_type_properties(self.raw, self.name)
