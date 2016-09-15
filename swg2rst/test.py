from __future__ import print_function

import codecs
import functools
import os, re
import inspect
import importlib
from io import StringIO as File_obj
from jinja2 import Environment, PackageLoader
from unittest import TestCase, SkipTest, main

from swg2rst.swagger.base_swagger_object import BaseSwaggerObject
from swg2rst.swagger.constants import SecurityTypes, SchemaTypes
from swg2rst.swagger.schema import Schema
from swg2rst.swagger.operation import Operation
from swg2rst.utils import rst
from swg2rst.utils import exampilators
try:
    import simplejson as json
except ImportError:
    import json

SAMPLES_PATH = os.path.join(os.path.dirname(__file__), os.pardir, 'samples')


class BaseSwaggerTestCase(object):

    swagger_filename = None
    swagger_doc = None
    example_filename = None
    examples = None

    @classmethod
    def setUpClass(cls):

        swagger_file = os.path.join(SAMPLES_PATH, cls.swagger_filename)
        with codecs.open(swagger_file, 'r', encoding='utf-8') as _file:
            doc = json.load(_file)

        if doc is None:
            raise SkipTest('File is empty')

        if cls.example_filename:
            example_file = os.path.join(SAMPLES_PATH, cls.example_filename)
            with codecs.open(example_file, 'r', encoding='utf-8') as _file:
                cls.examples = json.load(_file)

            if not cls.examples:
                raise SkipTest('Example file is empty')

        cls.swagger_doc = BaseSwaggerObject(doc)
        cls.exampilator = cls.swagger_doc.exampilator

    def test_swagger_root(self):
        map(functools.partial(self.assertIsInstance, cls=list), self.swagger_doc.tags.values())

        if 'parameters' in self.swagger_doc.raw:
            self.assertEqual(
                len(self.swagger_doc.raw['parameters']),
                len(self.swagger_doc.parameter_definitions)
            )

    def test_security_definitions(self):
        if 'securityDefinitions' in self.swagger_doc.raw:
            getting = sorted(self.swagger_doc.raw['securityDefinitions'].keys())
            expected = sorted(self.swagger_doc.security_definitions.keys())
            self.assertSequenceEqual(getting, expected)

    def test_doc_security(self):
        if 'security' in self.swagger_doc.raw:
            self._test_security(self.swagger_doc.security)

    def _test_security(self, security_obj):
        for key, security in security_obj.items():
            self.assertIn(key, self.swagger_doc.security_definitions)
            if security:
                # list is not empty
                security_def = self.swagger_doc.security_definitions[key]
                self.assertEqual(security_def.type, SecurityTypes.OAUTH2)

                # security scopes in security definition
                self.assertLessEqual(set(security), set(security_def.scopes))

    def test_schemas(self):

        definition_schemas = self.swagger_doc.schemas.get_schemas(
            [SchemaTypes.DEFINITION])
        self.assertEqual(len(definition_schemas), len(self.swagger_doc.raw['definitions']))

    def _get_definition_schema(self, name):
        schema_obj = self.swagger_doc.raw['definitions'][name]
        schema = Schema(
            schema_obj, SchemaTypes.DEFINITION, name=name, root=None, storage=self.swagger_doc.schemas)

        self.assertTrue(self.swagger_doc.schemas.contains(schema.schema_id))
        self.assertEqual(self.swagger_doc.schemas.get(schema.schema_id).name, name)

        return schema

    def test_operations(self):
        for path, operations in self.swagger_doc.raw['paths'].items():
            path_params_count = 0

            if 'parameters' in operations:
                self._check_parameters(operations['parameters'])
                path_params_count += len(operations['parameters'])

            for method, operation_obj in operations.items():
                if method == 'parameters':
                    continue
                operation_id = operation_obj.get(
                    'operationId', Operation.get_operation_id(method, path))
                self.assertIn(operation_id, self.swagger_doc.operations)

                operation = self.swagger_doc.operations[operation_id]
                self._test_parameters(operation_obj, operation, path_params_count)
                self._test_responses(operation_obj, operation)

                if 'security' in operation_obj:
                    self._test_security(operation.security)

    def test_primitive_examples(self):

        examples = self.exampilator.DEFAULT_EXAMPLES
        method = self.exampilator.get_example_value_for_primitive_type
        pairs = (
            (method('string', {}, ''), examples['string']),
            (method('string', {}, 'date'), examples['date']),
            (method('string', {}, 'date-time'), examples['date-time']),
            (method('', {'default': 'default'}, ''), 'default'),
            (method('', {'enum': [1, 2, 3]}, ''), 1),
            (method('integer', {}, ''), examples['integer']),
            (method('integer', {'minimum': 1000}, ''),
             examples['integer'] if examples['integer'] >= 1000 else 1000),
            (method('integer', {'maximum': -1000}, ''),
             examples['integer'] if examples['integer'] <= -1000 else -1000),
            (method('integer', {'minimum': 1000, 'exclusive_minimum': True}, ''),
             examples['integer'] if examples['integer'] > 1000 else 1001),
            (method('integer', {'maximum': -1000, 'exclusive_maximum': True}, ''),
             examples['integer'] if examples['integer'] < -1000 else -1001),
            (method('boolean', {}, ''), examples['boolean']),
        )
        for pair in pairs:
            self.assertEqual(*pair)

    def test_custom_examples(self):
        self.exampilator.fill_examples(self.examples)
        if 'types' in self.examples:
            for _type, value in self.examples['types'].items():
                self.assertEqual(self.exampilator.DEFAULT_EXAMPLES[_type], value)
        else:
            self.assertDictEqual(
                self.exampilator.DEFAULT_EXAMPLES, exampilators.DEFAULT_EXAMPLES)

        if 'array_items_count' in self.examples:
            self.assertEqual(self.exampilator.EXAMPLE_ARRAY_ITEMS_COUNT,
                             self.examples['array_items_count'])

        integer_example = self.examples['types'].get(
            'integer', exampilators.DEFAULT_EXAMPLES['integer'])
        len_examples = self.examples.get('array_items_count', 2)

        self.assertEqual(
            self.exampilator.get_example_for_array(
                {'type': 'integer', 'type_properties': {}, 'type_format': None}),
            [integer_example] * len_examples)

    def _test_parameters(self, operation_obj, operation, params_count):
        if 'parameters' in operation_obj:
            self._check_parameters(operation_obj['parameters'])
            params_count += len(operation_obj['parameters'])

        self.assertEqual(len(operation.parameters), params_count)
        self.assertEqual(len(operation.get_parameters_by_location()), params_count)

        if operation.get_parameters_by_location(['body']):
            self.assertIsNotNone(operation.body)
        else:
            self.assertIsNone(operation.body)

    def _test_responses(self, operation_obj, operation):
        self.assertEqual(len(operation_obj['responses']), len(operation.responses))
        for response in operation_obj['responses'].values():
            if '$ref' in response:
                self.assertIn(response['$ref'], self.swagger_doc.response_definitions)

    def _check_parameters(self, params_obj):
        for param in params_obj:
            if '$ref' in param:
                self.assertIn(param['$ref'], self.swagger_doc.parameter_definitions)

    def _make_operation(self, path, method):
        path_obj = self.swagger_doc.raw['paths'][path]

        operation_obj = path_obj[method]
        operation = Operation(
            operation_obj, method, path, self.swagger_doc, self.swagger_doc.schemas)

        return operation


class InstagramTestCase(BaseSwaggerTestCase, TestCase):

    swagger_filename = 'instagram.json'
    example_filename = 'instagram_examples.json'

    def test_custom_examples(self):
        super(InstagramTestCase, self).test_custom_examples()
        self.assertEqual(
            self.exampilator.CUSTOM_EXAMPLES['#/definitions/Media.likes.count'],
            self.examples['definitions']['#/definitions/Media']['likes.count']
        )

        self._test_schema_example()
        self._test_operation_example()

    def _test_schema_example(self):
        schema = self._get_definition_schema('MiniProfile')
        raw_definition = self.examples['definitions']['#/definitions/MiniProfile']
        self.assertEqual(self.exampilator.get_example_by_schema(schema), {
            'full_name': raw_definition['full_name'],
            'id': self.examples['types']['integer'],
            'profile_picture': self.examples['types']['string'],
            'user_name': raw_definition['user_name'],
        })

    def _test_operation_example(self):
        raw = self.examples['paths']['/users/{user-id}/relationship']['post']
        operation = self._make_operation('/users/{user-id}/relationship', 'post')

        self.assertEqual(self.exampilator.get_body_example(operation),
                         raw['parameters']['action'])

        self.assertSequenceEqual(
            self.exampilator.get_response_example(operation, operation.responses['200']),
            {'data': [raw['responses']['200.data']] * self.examples['array_items_count']}
        )


def iterate(generator, index):
    try:
        result = next(generator) or ' '
    except StopIteration:
        result = None
    index += 1
    return result, index


class RSTIntegrationsTestCase(TestCase):
    """
    Testing rst-specific methods
    """
    @staticmethod
    def prepare_env(cnt, file_name=True, inline=False):
        this = {}
        if file_name:
            this['file_name_json'] = os.path.join(SAMPLES_PATH, '{}.json'.format(cnt))
            this['file_name_rst'] = os.path.join(SAMPLES_PATH,
                                                 '{}{inline}.rst'.format(cnt, inline='_inline' if inline else '')
                                                 )
            with codecs.open(this['file_name_json'], 'r', encoding='utf-8') as _file:
                doc = json.load(_file)
        else:
            this['file_name_json'] = False
            this['file_name_rst'] = False
            doc = json.load(cnt)
        this['swagger_doc'] = rst.SwaggerObject(doc)
        doc_module = importlib.import_module('swg2rst.utils.rst')
        jinja_env = Environment(lstrip_blocks=True, trim_blocks=True)
        jinja_env.loader = PackageLoader('swg2rst')
        for name, function in inspect.getmembers(doc_module, inspect.isfunction):
            jinja_env.filters[name] = function
        jinja_env.filters['sorted'] = sorted
        template = jinja_env.get_template('main.rst')
        this['raw_rst'] = template.render(doc=this['swagger_doc'], inline=inline)
        this['pattern'] = re.compile(r'[idm]_\w{32}')
        this['normalize'] = lambda x: x[:-1] if x[-1] == '\n' else x
        return this

    @staticmethod
    def run_integration(this):
        log = []
        flag = None
        counter = 5
        original_i = 0
        generated_i = 0
        generated_lines = (i.strip() for i in this['raw_rst'].split('\n'))
        with codecs.open(this['file_name_rst'], 'r', encoding='utf-8') as _file:
            original_lines = (this['normalize'](i).strip() for i in _file.readlines())
        original_line, original_i = iterate(original_lines, original_i)
        generated_line, generated_i = iterate(generated_lines, generated_i)
        while generated_line or original_line:
            log.append('o{}:{}\ng{}:{}'.format(original_i, repr(original_line), generated_i, repr(generated_line)))
            if (len(log) > counter) and (not flag):
                log.pop(0)
            if (len(log) > 2 * counter - 1) and flag:
                print('\n'.join(log) + '\no:Original rst / g:Generated rst')
                raise Exception('Differences found at {} line!'.format(flag))
            if original_line == ' ' and generated_line == ' ':
                pass
            elif original_line != ' ' and generated_line == ' ':
                while generated_line == ' ':
                    generated_line, generated_i = iterate(generated_lines, generated_i)
            elif original_line == ' ' and generated_line != ' ':
                while original_line == ' ':
                    original_line, original_i = iterate(original_lines, original_i)
            else:
                if this['pattern'].search(original_line):
                    pass
                elif (original_line != generated_line) and (not flag):
                    flag = 'o{}/g{}'.format(original_i, generated_i)  # up flag

            original_line, original_i = iterate(original_lines, original_i)
            generated_line, generated_i = iterate(generated_lines, generated_i)

    @staticmethod
    def make_content():
        return File_obj(u"""{
  "swagger": "2.0",
  "info": {
    "version": "0.0.1",
    "description": "",
    "title": "API title"
  },
  "host": "",
  "basePath": "/",
  "produces": [
    "application/json"
  ],
  "consumes": [
    "application/json"
  ],
  "paths": {
    "/api/v1/short_path": {
      "get": {
        "responses": {
          "999": {
            "schema": {
              "type": "object",
                "properties": {
                  "ReferenceProperty": {
                    "additionalProperties": {
                      "$ref": "#/definitions/SimpleSerializer" 
                    }
                  }
                }
              }
            }
          }
        }
      }
    },
  "definitions": {
    "SimpleSerializer": {
      "type": "object",
      "properties": {
        "MyProp": {
          "type": "string"
        }
      }
    },
    "DifficultSerializer": {
      "schema": {
        "allOf": [
          {"$ref": "#/definitions/SimpleSerializer"},
          { "type": "object",
          "properties":{
            "YouProp": {
              "type": "string"
              }
            }
          }
        ]
      }
    }
  }
}""")

    def test_get_regular(self):
        """
        SwaggerObject.get_regular_properties
        """
        this = self.prepare_env(self.make_content(), file_name=False)
        result = this['swagger_doc'].get_regular_properties('d_3dccce5dab252608978d2313d304bfbd', definition=True)
        expect = """.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        MyProp | No | string |  |  |
"""
        assert(result.strip() == expect.strip())

    def test_get_type_definition(self):
        """SwaggerObject.get_type_description"""
        this = self.prepare_env(self.make_content(), file_name=False)
        result = this['swagger_doc'].get_type_description('d_3dccce5dab252608978d2313d304bfbd')
        expect = ':ref:`SimpleSerializer <d_3dccce5dab252608978d2313d304bfbd>`'
        assert(result == expect)

    def test_get_type_inline(self):
        """SwaggerObject.get_type_description"""
        this = self.prepare_env(self.make_content(), file_name=False)
        result = this['swagger_doc'].get_type_description('i_7886d86d0baffa0e753f35d813f3cec6')
        expect = ':ref:`ReferenceProperty <i_7886d86d0baffa0e753f35d813f3cec6>`'
        assert(result == expect)

    def test_get_additional(self):
        """SwaggerObject.get_additional_properties"""
        this = self.prepare_env(self.make_content(), file_name=False)
        result = this['swagger_doc'].get_additional_properties('i_7886d86d0baffa0e753f35d813f3cec6')
        expect = """
Map of {"key":":ref:`SimpleSerializer <d_3dccce5dab252608978d2313d304bfbd>`"}
"""
        assert(result.strip() == expect.strip())

    def test_additionalprop(self):
        file_name = 'additionalProperties'
        this = self.prepare_env(file_name)
        self.run_integration(this)

    def test_additionalprop_inline(self):
        file_name = 'additionalProperties'
        this = self.prepare_env(file_name, inline=True)
        self.run_integration(this)

    def test_intergation_allof(self):
        file_name = 'allOf'
        this = self.prepare_env(file_name)
        self.run_integration(this)

    def test_intergation_allof_inline(self):
        file_name = 'allOf'
        this = self.prepare_env(file_name, inline=True)
        self.run_integration(this)

    def test_intergation_instagram(self):
        file_name = 'instagram'
        this = self.prepare_env(file_name)
        self.run_integration(this)

    # def test_intergation_instagram_inline(self):
    #     #TODO: fixme. Unstable worked
    #     file_name = 'instagram'
    #     this = self.prepare_env(file_name, inline=True)
    #     self.run_integration(this)


if __name__ == '__main__':
    main()
