import json
from hashlib import md5
from collections import Mapping, Iterable
from .constants import SchemaTypes


class AbstractTypeObject(object):
    _type = None
    type_format = None
    properties = None
    item = None  #: set if type is array

    def __init__(self, obj, name, root, storage):
        self.raw = obj
        self.name = name
        self.root = root
        self.storage = storage

    def get_type_properties(self, property_obj, name, additional_prop=False):
        """ Get internal properties of property (extended in schema)

        :param dict property_obj: raw property object
        :param str name: name of property
        :param bool additional_prop: recursion's param
        :return: Type, format and internal properties of property
        :rtype: tuple(str, str, dict)
        """
        property_type = property_obj.get('type', 'object')
        property_format = property_obj.get('format')
        property_dict = {}

        if property_type in ['object', 'array']:
            schema_type = SchemaTypes.MAPPED if additional_prop else SchemaTypes.INLINE
            schema_id = self._get_object_schema_id(property_obj, schema_type)
            if not ('$ref' in property_obj or self.storage.get(schema_id)):
                _schema = self.storage.create_schema(
                    property_obj, name, schema_type, root=self.root)
                self._after_create_schema(_schema)
            property_type = schema_id

        property_dict['default'] = property_obj.get('default')
        property_dict['maximum'] = property_obj.get('maximum')
        property_dict['exclusive_maximum'] = property_obj.get('exclusiveMaximum')
        property_dict['minimum'] = property_obj.get('minimum')
        property_dict['exclusive_minimum'] = property_obj.get('exclusiveMinimum')
        property_dict['max_length'] = property_obj.get('maxLength')
        property_dict['min_length'] = property_obj.get('minLength')
        property_dict['enum'] = convert(property_obj.get('enum'))
        property_dict = {k: v for k, v in property_dict.items() if v}

        return property_type, property_format, property_dict

    @staticmethod
    def _get_id(base):
        m = md5()
        m.update(base.encode('utf-8'))
        return m.hexdigest()

    def _get_object_schema_id(self, obj, schema_type):
        if (schema_type == SchemaTypes.prefixes[SchemaTypes.MAPPED]) and ('$ref' in obj):
            base = obj['$ref']
            prefix = schema_type
        elif '$ref' in obj:
            base = obj['$ref']
            prefix = SchemaTypes.prefixes[SchemaTypes.DEFINITION]
        else:
            base = json.dumps(obj)
            prefix = SchemaTypes.prefixes[schema_type]
        return '{}_{}'.format(prefix, self._get_id(base))

    def set_type_by_schema(self, schema_obj, schema_type):
        """
        Set property type by schema object
        Schema will create, if it doesn't exists in collection

        :param dict schema_obj: raw schema object
        :param str schema_type:
        """
        schema_id = self._get_object_schema_id(schema_obj, schema_type)

        if not self.storage.contains(schema_id):
            schema = self.storage.create_schema(
                schema_obj, self.name, schema_type, root=self.root)
            assert schema.schema_id == schema_id
        self._type = schema_id

    def _after_create_schema(self, schema):
        pass

    @property
    def type(self):
        return self._type

    @property
    def is_array(self):
        return self._type == 'array'


def convert(data):
    """
    Convert from unicode to native ascii
    """
    try:
        st = basestring
    except NameError:
        st = str
    if isinstance(data, st):
        return str(data)
    elif isinstance(data, Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, Iterable):
        return type(data)(map(convert, data))
    else:
        return data
