# coding: utf-8

import sys
try:
    import pypandoc
except ImportError:
    WITH_PANDOC = False
else:
    WITH_PANDOC = True

from swg2rst.swagger import BaseSwaggerObject
from swg2rst.swagger import SchemaObjects
from swg2rst.swagger import SchemaMapWrapper
from swg2rst.swagger import PRIMITIVE_TYPES
from swg2rst.swagger import SchemaTypes
from swg2rst.swagger import Operation
from json import dumps

HEADERS = {1: '=', 2: '~', 3: '-', 4: '+', 5: '^'}


class SwaggerObject(BaseSwaggerObject):

    @staticmethod
    def sorted(collection):
        '''
        sorting dict by key,
        schema-collection by schema-name
        operations by id
        '''
        if len(collection) < 1:
            return collection

        if isinstance(collection, dict):
            return sorted(collection.items(), key=lambda x:x[0])

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
        if not SchemaObjects.contains(_type):
            return _type
        kwargs['post_callback'] = self._post_process_description
        schema = SchemaObjects.get(_type)
        if schema.schema_type == SchemaTypes.DEFINITION:
            if not kwargs.get('definition'):
                return ''
        head = '''.. _{}{}:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

'''.format(schema.schema_id, args[0] if args else '')
        body = []
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
        :param post_callback:
        :rtype: str
        """
        if not SchemaObjects.contains(_type):
            return _type
        kwargs['post_callback'] = self._post_process_description
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
            result = schema.name
            if kwargs.get('post_callback'):
                result = kwargs['post_callback'](result, schema, *args, **kwargs)
        return result

    def get_additional_properties(self, _type, *args, **kwargs):
        if not SchemaObjects.contains(_type):
            return _type
        kwargs['post_callback'] = self._post_process_description
        schema = SchemaObjects.get(_type)
        # link = '.. _i_65ee0248eafa0d637832fa3e8d9d388f:'
        head = '.. _{}{}:\n\n'.format(schema.schema_id, args[0] if args else '')
        body = []
        if schema.nested_schemas:
            for sch in schema.nested_schemas:
                nested_schema = SchemaObjects.get(sch)
                if not nested_schema:
                    return 'Error:\n{}'.format(repr(nested_schema))
                if isinstance(nested_schema, SchemaMapWrapper):
                    body.append('Map of {{"key":"{}"}}\n\n'.format(self.get_type_description(nested_schema.schema_id, *args, **kwargs)))
                    if nested_schema.item and nested_schema.item.get('type'):
                        if (nested_schema.item['type'] not in PRIMITIVE_TYPES) \
                                and (nested_schema.item['type'][0] != SchemaTypes.DEFINITION[0]):
                            body.append(self.get_regular_properties(nested_schema.item['type'], *args, **kwargs))
                    else:
                        body.append(self.get_regular_properties(nested_schema.schema_id, *args, **kwargs))
        elif schema.type_format:
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

def json_dumps(obj, *args, **kwargs):

    def sorter(obj):
        if isinstance(obj, dict):
            res = SwaggerObject.sorted(obj)
            for num, chunk in enumerate(res):
                res[num] = (chunk[0], sorter(chunk[1]))
            return dict(res) # <-- orederedDict needed
        return obj

    # res = sorter(obj)
    return dumps(obj, sort_keys=True, indent=kwargs.get('indent'))
