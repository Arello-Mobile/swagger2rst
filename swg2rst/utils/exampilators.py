# coding: utf-8

from jsonschema import (
    validate as schema_validate, FormatChecker, ValidationError, SchemaError)
from swg2rst.utils.logger import get_logger
from swg2rst.swagger.constants import PRIMITIVE_TYPES
from swg2rst.swagger.schemaObjects import SchemaObjects
from swg2rst.swagger.schema import SchemaMapWrapper

_DEFAULT_EXAMPLES = {
    'integer': 1,
    'number': 1.0,
    'string': 'somestring',
    'date': '2015-01-01',
    'date-time': '2015-01-01T15:00:00.000Z',
    'boolean': True,
    'password': '*****',
}

class Exampilator(object):
    """
    Example Manager
    """

    DEFAULT_EXAMPLES = _DEFAULT_EXAMPLES.copy()
    CUSTOM_EXAMPLES = dict()
    EXAMPLE_ARRAY_ITEMS_COUNT = 2

    logger = get_logger()
    _json_format_checker = FormatChecker()

    @classmethod
    def fill_examples(cls, examples):

        if 'array_items_count' in examples:
            cls.EXAMPLE_ARRAY_ITEMS_COUNT = examples['array_items_count']
        if 'types' in examples:
            cls.DEFAULT_EXAMPLES.update(examples['types'])
        if 'definitions' in examples:
            for path, fields in examples['definitions'].items():
                for field, value in fields.items():
                    key = '.'.join((path, field))
                    cls.CUSTOM_EXAMPLES[key] = value
        if 'paths' in examples:
            for path, methods in examples['paths'].items():
                key = "#/paths/'{}'".format(path)
                for method, operations in methods.items():
                    for section, fields in operations.items():
                        for field, value in fields.items():
                            _key = '/'.join((key, method, section, field))
                            cls.CUSTOM_EXAMPLES[_key] = value

    @classmethod
    def get_example_value_for_primitive_type(cls, type_, properties, format_, **kw):
        paths = kw.get('paths')
        if paths:
            result, path = cls._get_custom_example(paths)
            if result:
                cls._example_validate(path, result, type_, format_)
                return result

        if properties.get('default') is not None:
            result = properties['default']
        elif properties.get('enum'):
            result = properties['enum'][0]
        else:
            result = getattr(cls, '%s_example' % type_)(properties, format_)

        return result

    @classmethod
    def string_example(cls, properties, type_format):
        if type_format in cls.DEFAULT_EXAMPLES:
            result = cls.DEFAULT_EXAMPLES[type_format]
        else:
            result = cls.DEFAULT_EXAMPLES['string']

        if properties.get('min_length'):
            result.ljust(properties['min_length'], 'a')
        if properties.get('max_length'):
            result = result[:properties['max_length']]
        return result

    @classmethod
    def integer_example(cls, properties, *args):
        result = cls.DEFAULT_EXAMPLES['integer']
        if properties.get('minimum') is not None and result < properties['minimum']:
            result = properties['minimum']
            if properties.get('exclusive_minimum', False):
                result += 1
        elif properties.get('maximum') is not None and result > properties['maximum'] :
            result = properties['maximum']
            if properties.get('exclusive_maximum', False):
                result -= 1
        return result

    @classmethod
    def number_example(cls, properties, *args):
        return cls.integer_example(properties)

    @classmethod
    def boolean_example(cls, *args):
        return cls.DEFAULT_EXAMPLES['boolean']

    @classmethod
    def get_example_by_schema(cls, schema, ignored_schemas=None, paths=None, name=''):
        """ Get example by schema object

        :param Schema schema: current schema
        :param list ignored_schemas: list of previous schemas
            for avoid circular references
        :param list paths: list object paths (ex. #/definitions/Model.property)
            If nested schemas exists, custom examples checks in order from paths
        :param str name: name of property schema object if exists
        :return: dict or list (if schema is array)
        """
        if schema.schema_example:
            return schema.schema_example

        if ignored_schemas is None:
            ignored_schemas = []

        if paths is None:
            paths = []

        if name:
            paths = list(map(lambda path: '.'.join((path, name)), paths))

        if schema.ref_path:
            paths.append(schema.ref_path)

        if schema.schema_id in ignored_schemas:
            result = [] if schema.is_array else {}
        else:
            schemas = ignored_schemas + [schema.schema_id]
            kwargs = dict(
                ignored_schemas=schemas,
                paths=paths
            )
            if schema.is_array:
                result = cls.get_example_for_array(
                    schema.item, **kwargs)
            elif schema.type in PRIMITIVE_TYPES:
                result = cls.get_example_value_for_primitive_type(
                    schema.type, schema.raw, schema.type_format, paths=paths
                )
            elif schema.all_of:
                result = {}
                for _schema_id in schema.all_of:
                    schema = SchemaObjects.get(_schema_id)
                    result.update(cls.get_example_by_schema(schema, **kwargs))
            else:
                result = cls.get_example_for_object(
                    schema.properties, nested=schema.nested_schemas, **kwargs)
        return result

    @classmethod
    def get_body_example(cls, operation):
        """ Get example for body parameter example by operation

        :param Operation operation: operation object
        """
        path = "#/paths/'{0.path}'/{0.method}/parameters/{name}".format(
            operation, name=operation.body.name or 'body')
        return cls.get_example_by_schema(operation.body, paths=[path])

    @classmethod
    def get_response_example(cls, operation, response):
        """ Get example for response object by operation object

        :param Operation operation: operation object
        :param Response response: response object
        """
        path = "#/paths/'{}'/{}/responses/{}".format(
            operation.path, operation.method, response.name)
        kwargs = dict(paths=[path])

        if response.type in PRIMITIVE_TYPES:
            result = cls.get_example_value_for_primitive_type(
                response.type, response.properties, response.type_format, **kwargs)
        else:
            schema = SchemaObjects.get(response.type)
            result = cls.get_example_by_schema(schema, **kwargs)

        return result

    @classmethod
    def get_header_example(cls, header):
        """ Get example for header object

        :param Header header: Header object
        :return: example
        :rtype: dict
        """
        if header.is_array:
            result = cls.get_example_for_array(header.item)
        else:
            example_method = getattr(cls, '{}_example'.format(header.type))
            result = example_method(header.properties, header.type_format)
        return {header.name: result}

    @classmethod
    def get_property_example(cls, property_, nested=None, **kw):
        """ Get example for property

        :param dict property_:
        :return: example value
        """
        paths = kw.get('paths', None)
        name = kw.get('name', '')
        result = None
        if name and paths:
            paths = list(map(lambda path: '.'.join((path, name)), paths))
            result, path = cls._get_custom_example(paths)
            if result is not None and property_['type'] in PRIMITIVE_TYPES:
                cls._example_validate(
                    path, result, property_['type'], property_['type_format'])
                return result

        if SchemaObjects.contains(property_['type']):
            schema = SchemaObjects.get(property_['type'])
            if result is not None:
                if schema.is_array:
                    if not isinstance(result, list):
                        result = [result] * cls.EXAMPLE_ARRAY_ITEMS_COUNT
                else:
                    if isinstance(result, list):
                        cls.logger.warning(
                            'Example type mismatch in path {}'.format(schema.ref_path))
            else:
                result = cls.get_example_by_schema(schema, **kw)

            if (not result) and schema.nested_schemas:
                for _schema_id in schema.nested_schemas:
                    _schema = SchemaObjects.get(_schema_id)
                    if _schema:
                        if isinstance(_schema, SchemaMapWrapper):
                            result[_schema.name] = cls.get_example_by_schema(_schema, **kw)
                        elif _schema.nested_schemas:
                            for _schema__id in _schema.nested_schemas:
                                _schema_ = SchemaObjects.get(_schema__id)
                                if isinstance(_schema_, SchemaMapWrapper):
                                    result[_schema.name] = cls.get_example_by_schema(_schema_, **kw)
        else:
            result = cls.get_example_value_for_primitive_type(
                property_['type'],
                property_['type_properties'],
                property_['type_format'],
                **kw
            )
        return result

    @classmethod
    def _get_custom_example(cls, paths):
        if cls.CUSTOM_EXAMPLES:
            for path in paths:
                if path in cls.CUSTOM_EXAMPLES:
                    return cls.CUSTOM_EXAMPLES[path], path
        return None, ''

    @classmethod
    def get_example_for_array(cls, obj_item, **kw):
        return [cls.get_property_example(obj_item, **kw)] * cls.EXAMPLE_ARRAY_ITEMS_COUNT

    @classmethod
    def get_example_for_object(cls, properties, nested=None, **kw):
        result = {}
        if properties:
            for _property in properties:
                kw['name'] = _property['name']
                result[_property['name']] = cls.get_property_example(
                    _property, nested=nested, **kw)
        return result

    @classmethod
    def schema_validate(cls, obj, json_schema):
        schema_validate(obj, json_schema, format_checker=cls._json_format_checker)

    @classmethod
    def _example_validate(cls, path, value, type_, format_=None):
        _json_schema = {'type': type_}
        if format_:
            _json_schema['format'] = format_
        try:
            cls.schema_validate(value, _json_schema)
        except (ValidationError, SchemaError):
            cls.logger.warning('Example type mismatch in path {}'.format(path))
