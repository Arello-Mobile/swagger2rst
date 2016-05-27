class SchemaMapWrapper(Schema):
    """Dedicated class to store AdditionalProperties in schema
    """
    def __init__(self, obj, **kwargs):
        super(SchemaMapWrapper, self).__init__(obj, SchemaTypes.MAPPED, **kwargs)

    @staticmethod
    def wrap(schema):
        if isinstance(schema, Schema):
            schema.__class__ = SchemaMapWrapper
