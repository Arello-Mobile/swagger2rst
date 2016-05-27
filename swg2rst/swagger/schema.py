import json
from .abstractTypeObject import AbstractTypeObject
from .constants import SchemaTypes, PRIMITIVE_TYPES
from .schemaObjects import SchemaObjects


class Schema(AbstractTypeObject):
    """ Represents Swagger Schema Object
    """
    schema_id = None
    schema_type = None  #: definition or inline
    ref_path = None  #: path for definition schemas
    nested_schemas = None
    all_of = None

    def __init__(self, obj, schema_type, **kwargs):

        assert schema_type in SchemaTypes.prefixes
        super(Schema, self).__init__(obj, **kwargs)
        self.nested_schemas = set()
        self.schema_type = schema_type
        self.description = obj.get('description', '').replace('"', '\'')
        self._type = obj.get('type', 'object')
        # assert self._type in ('array', 'object')

        self.type_format = obj.get('format')
        self.schema_example = obj.get('example')
        self.read_only = obj.get('readOnly', False)
        self.external_docs = obj.get('externalDocs')

        if self._type in PRIMITIVE_TYPES:
            self.properties = [{
                'name': kwargs.get('name', ''),
                'description': obj.get('description', ''),
                'required': obj.get('required', False),
                'type': self.type,
                'type_format': self.type_format,
                'type_properties': self.get_type_properties(obj, '')[2],
            }]

        if schema_type == SchemaTypes.DEFINITION:
            self.ref_path = '#/definitions/{}'.format(self.name)

        if self.is_array:
            self.item = dict(zip(
                ('type', 'type_format', 'type_properties'),
                self.get_type_properties(obj['items'], self.name)
            ))
            self.name += '_array'
            if self.item['type'] not in PRIMITIVE_TYPES:
                self.nested_schemas.add(self.item['type'])

        if 'properties' in obj:
            self._set_properties()

        if 'allOf' in obj:
            self.all_of = []
            schema = None
            for _obj in obj['allOf']:
                _id = self._get_object_schema_id(_obj, SchemaTypes.INLINE)
                if not SchemaObjects.contains(_id):
                    schema = SchemaObjects.create_schema(_obj, 'inline', SchemaTypes.INLINE, self.root)
                    assert schema.schema_id == _id
                if len(self.all_of) > 0:
                    if schema:
                        result_obj = SchemaObjects.merge_schemas(SchemaObjects.get(self.all_of[-1]), schema)
                    else:
                        result_obj = SchemaObjects.merge_schemas(SchemaObjects.get(self.all_of[-1]), SchemaObjects.get(_id))
                self.all_of.append(_id)
                self.nested_schemas.add(_id)

        self._set_schema_id()

    def _set_schema_id(self):
        _id = self._get_id(self.ref_path or json.dumps(self.raw))
        self.schema_id = '{}_{}'.format(
            SchemaTypes.prefixes[self.schema_type], _id)

    def _set_properties(self):
        self.properties = []
        required_fields = self.raw.get('required', [])
        for name, property_obj in self.raw['properties'].items():
            property_type, property_format, prop = self.get_type_properties(property_obj, name)
            if property_type not in PRIMITIVE_TYPES:
                self.nested_schemas.add(property_type)

            _obj = {
                'name': name,
                'description': '',
                'required': name in required_fields,
                'type': property_type,
                'type_format': property_format,
                'type_properties': prop,
            }

            if 'description' in property_obj:
                _obj['description'] = property_obj['description'].replace('"', '\'')

            self.properties.append(_obj)

    def _after_create_schema(self, schema):
        pass

    @property
    def is_inline(self):
        return self.schema_type == SchemaTypes.INLINE

    @property
    def is_inline_array(self):
        return self.is_inline and self.is_array

    def __repr__(self):
        return self.name
