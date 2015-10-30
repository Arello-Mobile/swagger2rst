# coding: utf-8
from swg2rst.swagger import BaseSwaggerObject

HEADERS = {1: '=', 2: '~', 3: '-', 4: '+', 5: '^'}


class SwaggerObject(BaseSwaggerObject):

    def get_schema_description(self, schema_id):
        result = super(SwaggerObject, self).get_schema_description(schema_id)
        schema = self.schemas.get(schema_id)
        if not schema.is_array:
            result = ':ref:`{} <{}>`'.format(result, schema_id)
        return result


def header(value, header_value):
    return u'{}\n{}'.format(value, HEADERS[header_value] * len(value))


def md2rst(obj):
    try:
        import pypandoc
    except ImportError:
        return obj.replace('```', '\n')
    else:
        return pypandoc.convert(obj, to='rst', format='markdown')
