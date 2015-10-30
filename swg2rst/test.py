import codecs
import functools
import json
import os
from unittest import TestCase, SkipTest, main

from swg2rst import swagger


SAMPLES_PATH = os.path.join(os.path.dirname(__file__), os.pardir, 'samples')


class BaseSwaggerTestCase(object):

    swagger_filename = None
    swagger_doc = None

    @classmethod
    def setUpClass(cls):

        swagger_file = os.path.join(SAMPLES_PATH, cls.swagger_filename)
        with codecs.open(swagger_file, 'r', encoding='utf-8') as _file:
            doc = json.load(_file)

        if doc is None:
            raise SkipTest('File is empty')

        cls.swagger_doc = swagger.BaseSwaggerObject(doc)

    def test_swagger_root(self):
        map(functools.partial(self.assertIsInstance, cls=list), self.swagger_doc.tags.values())

        if 'parameters' in self.swagger_doc.raw:
            self.assertEqual(
                len(self.swagger_doc.raw['parameters']),
                len(self.swagger_doc.parameter_definitions)
            )

    def test_security_definitions(self):
        if 'securityDefinitions' in self.swagger_doc.raw:
            self.assertItemsEqual(
                self.swagger_doc.raw['securityDefinitions'].keys(),
                self.swagger_doc.security_definitions.keys()
            )

    def test_doc_security(self):
        if 'security' in self.swagger_doc.raw:
            self._test_security(self.swagger_doc.security)

    def _test_security(self, security_obj):
        for key, security in security_obj.items():
            self.assertIn(key, self.swagger_doc.security_definitions)
            if security:
                # list is not empty
                security_def = self.swagger_doc.security_definitions[key]
                self.assertEqual(security_def.type, swagger.SecurityTypes.OAUTH2)

                # security scopes in security definition
                self.assertLessEqual(set(security), set(security_def.scopes))

    def test_schemas(self):

        definition_schemas = self.swagger_doc.schemas.get_schemas(
            [swagger.SchemaTypes.DEFINITION])
        self.assertEqual(len(definition_schemas), len(self.swagger_doc.raw['definitions']))

    def _get_definition_schema(self, name):
        schema_obj = self.swagger_doc.raw['definitions'][name]
        schema = swagger.Schema(schema_obj, name, swagger.SchemaTypes.DEFINITION)

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
                    'operationId', swagger.Operation.get_operation_id(method, path))
                self.assertIn(operation_id, self.swagger_doc.operations)

                operation = self.swagger_doc.operations[operation_id]
                self._test_parameters(operation_obj, operation, path_params_count)
                self._test_responses(operation_obj, operation)

                if 'security' in operation_obj:
                    self._test_security(operation.security)

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
        operation = swagger.Operation(
            operation_obj, method, path, self.swagger_doc)

        return operation


class InstagramTestCase(BaseSwaggerTestCase, TestCase):

    swagger_filename = 'instagram.json'


if __name__ == '__main__':
    main()
