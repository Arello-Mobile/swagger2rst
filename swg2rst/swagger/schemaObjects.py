from operator import attrgetter
from .constants import SchemaTypes
from .schema import Schema, SchemaMapWrapper


class SchemaObjects(object):
    """
    Schema collection
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
            schema = SchemaMapWrapper(obj, storage=cls, name=name, root=root)
        else:
            schema = Schema(obj, schema_type, storage=cls, name=name, root=root)
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
        return _schema

