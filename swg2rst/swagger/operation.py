import re
from swg2rst.converter_exceptions import ConverterError
from cached_property import cached_property
from .securityMixin import SecurityMixin
from .parameter import Parameter
from .response import Response


class Operation(SecurityMixin):
    """
    Represents Swagger Operation Object
    """
    parameters = None
    responses = None
    method = None
    path = None
    root = None  #: root swagger object

    def __init__(self, obj, method, path, root, storage, path_params=None):
        self.method = method
        self.path = path
        self.root = root
        self.storage = storage

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
        op_id = re.sub(r'[\s!@#$%^&*()+=\[{\]};:<>|./?,\'"-]', '_', op_id)
        op_id = re.sub(r'(_){2,}', '_', op_id)
        op_id = re.sub(r'^[_]*', '', op_id)
        op_id = re.sub(r'([_]*)$', '', op_id)

        return op_id

    def _fill_parameters(self, params, path_params):
        self.parameters = []
        for obj in params:
            if '$ref' in obj:
                self.parameters.append(self.root.parameter_definitions[obj['$ref']])
            else:
                self.parameters.append(
                    Parameter(obj, name=obj['name'], root=self.root, storage=self.storage))
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
                self.responses[code] = Response(obj, name=code, root=self.root, storage=self.storage)

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
