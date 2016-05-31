# coding: utf-8

import sys
try:
    import pypandoc
except ImportError:
    WITH_PANDOC = False
else:
    WITH_PANDOC = True

from swg2rst.swagger.base_swagger_object import BaseSwaggerObject
from swg2rst.swagger.schema_objects import SchemaObjects
from swg2rst.swagger.schema import SchemaMapWrapper
from swg2rst.swagger.constants import SchemaTypes
from swg2rst.swagger.operation import Operation
from json import dumps

HEADERS = {1: '=', 2: '~', 3: '-', 4: '+', 5: '^'}


class SwaggerObject(BaseSwaggerObject):

    @staticmethod
    def sorted(collection):
        """
        sorting dict by key,
        schema-collection by schema-name
        operations by id
        """
        if len(collection) < 1:
            return collection

        if isinstance(collection, dict):
            return sorted(collection.items(), key=lambda x: x[0])

        tmp = {}
        if isinstance(list(collection)[0], Operation):
            for item in collection:
                tmp[item.operation_id] = item
            tmp = sorted(tmp.items(), key=lambda x: x[0])
            return (x[1] for x in tmp)

        if isinstance(list(collection)[0], str):
            for item in collection:
                if SchemaObjects.get(item):
                    tmp[item] = SchemaObjects.get(item).name
                else:
                    sys.stderr.write('Something wrong with schema {}\n'.format(item))
            tmp = sorted(tmp.items(), key=lambda x: x[1])
            return (x[0] for x in tmp)

    def get_regular_properties(self, _type, *args, **kwargs):
        """Make table with properties by schema_id
        :param str _type:
        :rtype: str
        """
        if not SchemaObjects.contains(_type):
            return _type
        schema = SchemaObjects.get(_type)
        if schema.schema_type == SchemaTypes.DEFINITION and not kwargs.get('definition'):
            return ''
        head = """.. _{}{}:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

""".format(schema.schema_id, args[0] if args else '')
        body = []
        if schema.properties:
            for p in schema.properties:
                body.append('        {} | {} | {} | {} | {} | {} \n'.format(
                    p.get('name') or '',
                    'Yes' if p.get('required') else 'No',
                    self.get_type_description(p['type'], *args, **kwargs),
                    p.get('type_format') or '',
                    '{}'.format(p.get('type_properties') or ''),
                    p.get('description') or '')
                )
            body.sort()
        return head + ''.join(body)

    def get_type_description(self, _type, *args, **kwargs):
        """ Get description of type
        :param str _type:
        :rtype: str
        """
        if not SchemaObjects.contains(_type):
            return _type
        schema = SchemaObjects.get(_type)
        if schema.all_of:
            models = ','.join(
                (self.get_type_description(_type, *args, **kwargs) for _type in schema.all_of)
            )
            result = '{}'.format(models.split(',')[0])
            for r in models.split(',')[1:]:
                result += ' extended {}'.format(r)
        elif schema.is_array:
            result = 'array of {}'.format(
                self.get_type_description(schema.item['type'], *args, **kwargs))
        else:
            result = self._post_process_description(schema.name, schema, *args, **kwargs)
        return result

    def get_additional_properties(self, _type, *args, **kwargs):
        """Make head and table with additional properties by schema_id
        :param str _type:
        :rtype: str
        """
        if not SchemaObjects.contains(_type):
            return _type
        schema = SchemaObjects.get(_type)
        head = '.. _{}{}:\n\n'.format(schema.schema_id, args[0] if args else '')
        body = []
        for sch in schema.nested_schemas:  # complex types
            nested_schema = SchemaObjects.get(sch)
            if not (nested_schema or isinstance(nested_schema, SchemaMapWrapper)):
                continue

            body.append('Map of {{"key":"{}"}}\n\n'.format(self.get_type_description(
                nested_schema.schema_id, *args, **kwargs))  # head
            )
            if nested_schema.is_array:  # table
                _schema = SchemaObjects.get(nested_schema.item.get('type'))
                if _schema and _schema.schema_type == SchemaTypes.INLINE:
                    body.append(self.get_regular_properties(_schema.schema_id, *args, **kwargs))
            else:
                body.append(self.get_regular_properties(nested_schema.schema_id, *args, **kwargs))
        if schema.type_format:  # basic types, only head
            body.append(
                'Map of {{"key":"{}"}}'.format(self.get_type_description(schema.type_format, *args, **kwargs)))
        return head + ''.join(body)

    @staticmethod
    def _post_process_description(result, schema, *args, **kwargs):
        suffix = kwargs.get('suffix') or args and args[0] or ''
        if not schema.is_array and not schema.all_of:
            result = ':ref:`{} <{}{}>`'.format(result, schema.schema_id, suffix)
        return result


def header(value, header_value):
    return u'{}\n{}'.format(value, HEADERS[header_value] * len(value))


def md2rst(obj):
    if WITH_PANDOC:
        return pypandoc.convert(obj, to='rst', format='markdown')
    else:
        return obj.replace('```', '\n')


def json_dumps(obj, **kwargs):
    return dumps(obj, sort_keys=True, indent=kwargs.get('indent'))
