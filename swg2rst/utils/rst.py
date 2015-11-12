# coding: utf-8
try:
    import pypandoc
except ImportError:
    WITH_PANDOC = False
else:
    WITH_PANDOC = True

from swg2rst.swagger import BaseSwaggerObject

HEADERS = {1: '=', 2: '~', 3: '-', 4: '+', 5: '^'}


class SwaggerObject(BaseSwaggerObject):

    def get_type_description(self, _type, *args, **kwargs):
        kwargs['post_callback'] = self._post_process_description
        return self.schemas.get_type_description(_type, *args, **kwargs)

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
