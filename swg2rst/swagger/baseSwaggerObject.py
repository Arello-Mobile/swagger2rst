from collections import defaultdict
from jsonschema import ValidationError
from swg2rst.converter_exceptions import ConverterError
from swg2rst.utils.exampilators import Exampilator

from .securityMixin import SecurityMixin
from .schemaObjects import SchemaObjects
from .schema import Schema, SchemaMapWrapper
from .constants import PRIMITIVE_TYPES, SchemaTypes, examples_json_schema
from .parameter import Parameter
from .operation import Operation
from .response import Response
from .securityDefinition import SecurityDefinition


class BaseSwaggerObject(SecurityMixin):
    """
    Represents Swagger Object
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
                        Parameter(param, name=param['name'], root=self, storage=self.schemas))
            for method, operation in operations.items():
                if method == 'parameters':
                    continue
                op = Operation(operation, method, path, self, self.schemas, path_params)
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
        """At first create schemas without 'AllOf'
        :param obj:
        :return: None
        """
        self.schemas.clear()
        all_of_stack = []
        for name, definition in obj.items():
            if 'allOf' in definition:
                all_of_stack.append((name, definition))
            else:
                self.schemas.create_schema(
                    definition, name, SchemaTypes.DEFINITION, root=self)
        while all_of_stack:
            name, definition = all_of_stack.pop(0)
            self.schemas.create_schema(
                definition, name, SchemaTypes.DEFINITION, root=self)

    def _fill_parameter_definitions(self, obj):
        self.parameter_definitions = {}
        for name, parameter in obj.items():
            key = '#/parameters/{}'.format(name)
            self.parameter_definitions[key] = Parameter(
                parameter, name=parameter['name'], root=self, storage=self.schemas)

    def _fill_response_definitions(self, obj):
        self.response_definitions = {}
        for name, response in obj.items():
            key = '#/responses/{}'.format(name)
            self.response_definitions[key] = Response(
                response, name=name, root=self, storage=self.schemas)

    def _fill_security_definitions(self, obj):
        self.security_definitions = {
            name: SecurityDefinition(name, _obj) for name, _obj in obj.items()
        }
