{% if schema_link %}

.. _{{ schema.schema_id }}:

{% endif %}

{{ schema_header }}

{% if schema.type == 'array' %}

{{ doc.get_type_description(schema.item['type']) }}

{% endif %}

{% if schema.properties %}

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

    {% for p in schema.properties %}
        {{
            ' | '.join((
                p['name'],
                'Yes' if p['required'] else 'No',
                doc.get_type_description(p['type']),
                p['type_format'] or '',
                '{}'.format(p['type_properties']) if p['type_properties'] else '',
                p['description']
            ))

                }}
    {% endfor %}

{% else %}

{{ 'Empty object ({})' }}

{% endif %}

{% for schema_id in schema.nested_schemas %}
    {% set schema = doc.schemas.get(schema_id) %}
    {% if schema.is_inline and not schema.is_array %}
        {% set schema_header = '**{} schema:**'.format(schema.name)|capitalize %}

{% include "schema.rst"%}

    {% endif %}
{% endfor %}
