PRIMITIVE_TYPES = ('integer', 'number', 'string', 'boolean')


#: json validation schema for examples file
examples_json_schema = {
    'type': 'object',
    'properties': {
        'array_items_count': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 5
        },
        'types': {
            'type': 'object',
            'properties': {
                'string': {
                    'type': 'string'
                },
                'date': {
                    'type': 'string',
                    'format': 'date'
                },
                'date-time': {
                    'type': 'string',
                    'format': 'date-time'
                },
                'integer': {
                    'type': 'integer'
                },
                'number': {
                    'type': 'number'
                },
                'boolean': {
                    'type': 'boolean'
                }
            },
            'additionalProperties': False
        },
        'definitions': {
            'type': 'object',
            'patternProperties': {
                '^#/definitions/\w+$': {
                    'type': 'object'
                }
            },
            'additionalProperties': False
        },
        'paths': {
            'type': 'object',
            'patternProperties': {
                '^/': {
                    'type': 'object',
                    'patternProperties': {
                        '^[a-z]{,7}$': {
                            'type': 'object',
                            'properties': {
                                'parameters': {
                                    'type': 'object'
                                },
                                'responses': {
                                    'type': 'object'
                                }
                            },
                            'additionalProperties': False
                        }
                    },
                    'additionalProperties': False
                }
            },
            'additionalProperties': False
        }
    },
    'additionalProperties': False,
}


class SchemaTypes(object):
    """ Types of the schema object
    """
    INLINE = 'inline'
    DEFINITION = 'definition'
    MAPPED = 'mapped'

    prefixes = {
        INLINE: INLINE[0],
        DEFINITION: DEFINITION[0],
        MAPPED: MAPPED[0],
    }


class SecurityTypes(object):
    """ Types of the security scheme
    """
    BASIC = 'basic'
    OAUTH2 = 'oauth2'
    API_KEY = 'apiKey'

    names = {
        BASIC: 'HTTP Basic Authentication',
        OAUTH2: 'OAuth 2.0',
        API_KEY: 'API Key',
    }
