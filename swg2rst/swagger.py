import json
import re
from collections import defaultdict, Mapping, Iterable
from hashlib import md5
from operator import attrgetter

from cached_property import cached_property
from jsonschema import ValidationError

from swg2rst.converter_exceptions import ConverterError
from swg2rst.utils.exampilators import Exampilator

PRIMITIVE_TYPES = ('integer', 'number', 'string', 'boolean')

#: json validation schema for examples file
examples_json_schema = {
    'type': 'object',
    'properties': {
        'array_items_count': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 5
        },
        'types': {
            'type': 'object',
            'properties': {
                'string': {
                    'type': 'string'
                },
                'date': {
                    'type': 'string',
                    'format': 'date'
                },
                'date-time': {
                    'type': 'string',
                    'format': 'date-time'
                },
                'integer': {
                    'type': 'integer'
                },
                'number': {
                    'type': 'number'
                },
                'boolean': {
                    'type': 'boolean'
                }
            },
            'additionalProperties': False
        },
        'definitions': {
            'type': 'object',
            'patternProperties': {
                '^#/definitions/\w+$': {
                    'type': 'object'
                }
            },
            'additionalProperties': False
        },
        'paths': {
            'type': 'object',
            'patternProperties': {
                '^/': {
                    'type': 'object',
                    'patternProperties': {
                        '^[a-z]{,7}$': {
                            'type': 'object',
                            'properties': {
                                'parameters': {
                                    'type': 'object'
                                },
                                'responses': {
                                    'type': 'object'
                                }
                            },
                            'additionalProperties': False
                        }
                    },
                    'additionalProperties': False
                }
            },
            'additionalProperties': False
        }
    },
    'additionalProperties': False,
}


class SchemaTypes(object):
    """ Types of the schema object
    """
    INLINE = 'inline'
    DEFINITION = 'definition'
    MAPPED = 'mapped'

    prefixes = {
        INLINE: INLINE[0],
        DEFINITION: DEFINITION[0],
        MAPPED: MAPPED[0],
    }


class SecurityTypes(object):
    """ Types of the security scheme
    """
    BASIC = 'basic'
    OAUTH2 = 'oauth2'
    API_KEY = 'apiKey'

    names = {
        BASIC: 'HTTP Basic Authentication',
        OAUTH2: 'OAuth 2.0',
        API_KEY: 'API Key',
    }

class SchemaObjects(object):
    """ Schema collection
    """

    _schemas = dict()

    @classmethod
    def create_schema(cls, obj, name, schema_type, root):
        """ Create Schema object

        :param dict obj: swagger schema object
        :param str name: schema name
        :param str schema_type: schema location.
            Can be ``inline``, ``definition`` or ``mapped``
        :param BaseSwaggerObject root: root doc
        :return: new schema
        :rtype: Schema
        """
        if schema_type == SchemaTypes.MAPPED:
            schema = SchemaMapWrapper(obj, name=name, root=root)
        else:
            schema = Schema(obj, schema_type, name=name, root=root)
        cls.add_schema(schema)
        return schema

    @classmethod
    def add_schema(cls, schema):
        """ Add schema object to collection

        :param Schema schema:
        """
        cls._schemas[schema.schema_id] = schema

    @classmethod
    def get(cls, schema_id):
        """ Get schema object from collection by id

        :param str schema_id:
        :return: schema
        :rtype: Schema
        """
        return cls._schemas.get(schema_id)

    @classmethod
    def get_schemas(cls, schema_types=None, sort=True):
        """
        Get schemas by type. If ``schema_type`` is None, return all schemas

        :param schema_types: list of schema types
        :type schema_types: list or None
        :param bool sort: sort by name
        :return: list of schemas
        :rtype: list
        """
        result = filter(lambda x: not x.is_inline_array, cls._schemas.values())
        if schema_types:
            result = filter(lambda x: x.schema_type in schema_types, result)
        if sort:
            result = sorted(result, key=attrgetter('name'))
        return result

    @classmethod
    def contains(cls, key):
        """ Check schema existence in collection by id

        :param str key:
        :rtype: bool
        """
        return key in cls._schemas

    @classmethod
    def clear(cls):
        cls._schemas = dict()

    @classmethod
    def merge_schemas(cls, schema, _schema):
        """Return second Schema, which is extended by first Schema
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#composition-and-inheritance-polymorphism
        """
        assert  schema._type == 'object'
        assert _schema._type == 'object'
        tmp = schema.properties[:] # copy
        prop = {}
        to_dict = lambda e: prop.update({e.pop('name'): e})
        [to_dict(i) for i in tmp] # map(to_dict, tmp)
        for _prop in _schema.properties:
            if prop.get(_prop['name']):
                prop.pop(_prop['name'])
        if prop:
            for k, v in prop.items():
                v['name'] = k
                _schema.properties.append(v)
        # d = _schema.properties
        return _schema


class SecurityMixin(object):

    security = None

    def _fill_securities(self, obj):
        self.security = {}
        for security in obj:
            self.security.update(security)


class BaseSwaggerObject(SecurityMixin):
    """ Represents Swagger Object
    """
    raw = None

    #: Operation collection
    #:
    #: key: operation_id, value: Operation object
    operations = None

    #: Operations grouped by tags
    #:
    #: key: tag name, value: list of Operation object
    tags = None

    schemas = SchemaObjects

    #: Parameter definitions from Parameters Definitions Object
    #:
    #: key: reference path, value: Parameter object
    parameter_definitions = None

    #: Response definitions from Responses Definitions Object
    #:
    #: key: reference path, value: Response object
    response_definitions = None

    #: Security definitions from Security Definitions Object
    #:
    #: key: security name, value: SecurityDefinition object
    security_definitions = None

    #: Represents tag descriptions from Swagger Tag Object
    #:
    #: key: tag name, value: dict with keys ``description`` and ``externalDocs``
    tag_descriptions = None

    #: Example Manager. Must be subclass of Exampilator
    exampilator = None

    def __init__(self, obj, exampilator=None, examples=None):
        if obj['swagger'] != '2.0':
            raise ConverterError('Invalid Swagger version')

        self.raw = obj
        self.exampilator = exampilator or Exampilator
        assert issubclass(self.exampilator, Exampilator)
        self.exampilator(PRIMITIVE_TYPES, SchemaObjects, SchemaMapWrapper)
        if examples:
            try:
                self.exampilator.schema_validate(examples, examples_json_schema)
            except ValidationError as err:
                raise ConverterError(err.message)

            self.exampilator.fill_examples(examples)

        if 'definitions' in obj:
            self._fill_schemas_from_definitions(obj['definitions'])

        if 'parameters' in obj:
            self._fill_parameter_definitions(obj['parameters'])

        if 'responses' in obj:
            self._fill_response_definitions(obj['responses'])

        if 'securityDefinitions' in obj:
            self._fill_security_definitions(obj['securityDefinitions'])

        if 'security' in obj:
            self._fill_securities(obj['security'])

        self.info = obj['info']
        self.host = obj.get('host', '')
        self.base_path = obj.get('basePath', '')
        self.consumes = obj.get('consumes', ['application/json'])
        self.produces = obj.get('produces', ['application/json'])
        self.schemes = obj.get('schemes', ['http'])
        self._fill_operations()
        self.external_docs = obj.get('externalDocs')

    def _fill_operations(self):
        self.operations = {}
        self._fill_tag_descriptions()
        self.tags = defaultdict(list)
        for path, operations in self.raw['paths'].items():
            path_params = []
            for param in operations.get('parameters', []):
                if param.get('$ref'):
                    path_params.append(self.parameter_definitions[param['$ref']])
                else:
                    path_params.append(
                        Parameter(param, name=param['name'], root=self))
            for method, operation in operations.items():
                if method == 'parameters':
                    continue
                op = Operation(operation, method, path, self, path_params)
                self.operations[op.operation_id] = op
                for tag in op.tags:
                    self.tags[tag].append(op)

    def _fill_tag_descriptions(self):
        if 'tags' in self.raw:
            self.tag_descriptions = {}
            for tag in self.raw['tags']:
                if 'description' in tag or 'externalDocs' in tag:
                    self.tag_descriptions[tag['name']] = {
                        'description': tag.get('description'),
                        'externalDocs': tag.get('externalDocs')
                    }

    def _fill_schemas_from_definitions(self, obj):
        self.schemas.clear()
        allOf_stack = []
        for name, definition in obj.items():
            if 'allOf' in definition:
                allOf_stack.append( (name, definition) )
            else:
                self.schemas.create_schema(
                    definition, name, SchemaTypes.DEFINITION, root=self)
        while allOf_stack:
            name, definition = allOf_stack.pop(0)
            new_schema = Schema(definition, 'definition', name=name, root=self)
            self.schemas._schemas[new_schema.schema_id] = new_schema

    def _fill_parameter_definitions(self, obj):
        self.parameter_definitions = {}
        for name, parameter in obj.items():
            key = '#/parameters/{}'.format(name)
            self.parameter_definitions[key] = Parameter(
                parameter, name=parameter['name'], root=self)

    def _fill_response_definitions(self, obj):
        self.response_definitions = {}
        for name, response in obj.items():
            key = '#/responses/{}'.format(name)
            self.response_definitions[key] = Response(
                response, name=name, root=self)

    def _fill_security_definitions(self, obj):
        self.security_definitions = {
            name: SecurityDefinition(name, _obj) for name, _obj in obj.items()
        }


class Operation(SecurityMixin):
    """ Represents Swagger Operation Object
    """
    parameters = None
    responses = None
    method = None
    path = None
    root = None  #: root swagger object

    def __init__(self, obj, method, path, root, path_params=None):
        self.method = method
        self.path = path
        self.root = root

        self.operation_id = obj.get(
            'operationId', self.get_operation_id(method, path))

        self.summary = obj.get('summary')
        self.description = obj.get('description')
        self.consumes = obj.get('consumes', self.root.consumes)
        self.produces = obj.get('produces', self.root.produces)
        self.schemes = obj.get('schemes', self.root.schemes)
        self._fill_parameters(obj.get('parameters', []), path_params)
        self._fill_responses(obj['responses'])

        self.deprecated = obj.get('deprecated', False)

        self.tags = obj.get('tags', ['default'])
        self.external_docs = obj.get('externalDocs')

        if 'security' in obj:
            self._fill_securities(obj['security'])

    @staticmethod
    def get_operation_id(method, path):
        op_id = '{}_{}'.format(method, path)

        # copy-paste from swagger-js
        op_id = re.sub('[\s!@#$%^&*()+=\[{\]};:<>|./?,\'"-]', '_', op_id)
        op_id = re.sub('(_){2,}', '_', op_id)
        op_id = re.sub('^[_]*', '', op_id)
        op_id = re.sub('([_]*)$', '', op_id)

        return op_id

    def _fill_parameters(self, params, path_params):
        self.parameters = []
        for obj in params:
            if '$ref' in obj:
                self.parameters.append(self.root.parameter_definitions[obj['$ref']])
            else:
                self.parameters.append(
                    Parameter(obj, name=obj['name'], root=self.root))
        if path_params:
            self.parameters += path_params
        if len(self.get_parameters_by_location(['body'])) > 1:
            raise ConverterError(
                'Invalid source file: More than one body parameters in %s' % self.path)

    def _fill_responses(self, responses):
        self.responses = {}
        for code, obj in responses.items():
            if '$ref' in obj:
                self.responses[code] = self.root.response_definitions[obj['$ref']]
            else:
                self.responses[code] = Response(obj, name=code, root=self.root)

    def get_parameters_by_location(self, locations=None, excludes=None):
        """ Get parameters list by location

        :param locations: list of locations
        :type locations: list or None
        :param excludes: list of excludes locations
        :type excludes: list or None
        :return: list of Parameter
        :rtype: list
        """
        result = self.parameters
        if locations:
            result = filter(lambda x: x.location_in in locations, result)
        if excludes:
            result = filter(lambda x: x.location_in not in excludes, result)
        return list(result)

    @cached_property
    def body(self):
        """ Return body request parameter

        :return: Body parameter
        :rtype: Parameter or None
        """
        body = self.get_parameters_by_location(['body'])
        return self.root.schemas.get(body[0].type) if body else None


class AbstractTypeObject(object):

    _type = None
    type_format = None
    properties = None
    item = None  #: set if type is array

    def __init__(self, obj, name, root, **kwargs):
        self.raw = obj
        self.name = name
        self.root = root

    def get_type_properties(self, property_obj, name, additional_prop=False):
        """ Get internal properties of property

        :param dict property_obj: raw property object
        :param str name: name of property
        :return: Type, format and internal properties of property
        :rtype: tuple(str, str, dict)
        """

        def convert(data):
            '''
            Convert from unicode to native ascii
            '''
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

        property_type = property_obj.get('type', 'object')
        property_format = property_obj.get('format')
        property_dict = dict()
        _schema = None

        if property_type in ['object', 'array']:
            schema_type = SchemaTypes.MAPPED if additional_prop else SchemaTypes.INLINE
            schema_id = self._get_object_schema_id(property_obj, schema_type)
            if not ('$ref' in property_obj or SchemaObjects.get(schema_id)):
                _schema = SchemaObjects.create_schema(
                    property_obj, name, schema_type, root=self.root)
                self._after_create_schema(_schema)
            property_type = schema_id

        if 'default' in property_obj:
            property_dict['default'] = property_obj['default']

        if 'maximum' in property_obj:
            property_dict['maximum'] = property_obj['maximum']
            property_dict['exclusive_maximum'] = property_obj.get('exclusiveMaximum', False)

        if 'minimum' in property_obj:
            property_dict['minimum'] = property_obj['minimum']
            property_dict['exclusive_minimum'] = property_obj.get('exclusiveMinimum', False)

        if 'maxLength' in property_obj:
            property_dict['max_length'] = property_obj['maxLength']

        if 'minLength' in property_obj:
            property_dict['min_length'] = property_obj['minLength']

        if 'enum' in property_obj:
            property_dict['enum'] = convert(property_obj['enum'])

        if 'additionalProperties' in property_obj:
            _property_type, _property_format, _property_dict = self.get_type_properties(
                property_obj['additionalProperties'], '{}-mapped'.format(name), additional_prop=True)
            if _property_type not in PRIMITIVE_TYPES:
                SchemaMapWrapper.wrap(SchemaObjects.get(_property_type))
                _schema.nested_schemas.add(_property_type)
            else:
                _schema.type_format = _property_type

        return property_type, property_format, property_dict

    @staticmethod
    def _get_id(base):
        m = md5()
        m.update(base.encode('utf-8'))
        return m.hexdigest()

    def _get_object_schema_id(self, obj, schema_type):
        if (schema_type == SchemaTypes.prefixes[SchemaTypes.MAPPED])\
            and ('$ref' in obj):
            base = obj['$ref']
            prefix = schema_type
        elif ('$ref' in obj):
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
        """
        schema_id = self._get_object_schema_id(schema_obj, schema_type)

        if not SchemaObjects.contains(schema_id):
            schema = SchemaObjects.create_schema(
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


class Header(AbstractTypeObject):
    """ Represents Swagger Header Object
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


class SchemaMapWrapper(Schema):
    """Dedicated class to store AdditionalProperties in schema
    """
    def __init__(self, obj, **kwargs):
        super(SchemaMapWrapper, self).__init__(obj, SchemaTypes.MAPPED, **kwargs)

    @staticmethod
    def wrap(schema):
        if isinstance(schema, Schema):
            schema.__class__ = SchemaMapWrapper

class SecurityDefinition(object):
    """ Represents Swagger Security Scheme Object
    """
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
