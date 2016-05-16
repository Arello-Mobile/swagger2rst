{% if schema_link or inline %}

.. _{{ '{}{}'.format(schema.schema_id, definition_suffix) }}:

{% endif %}

{{ schema_header }}

{% if schema.type == 'array' %}

{{ doc.get_type_description(schema.item['type'], definition_suffix) }}

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
                doc.get_type_description(p['type'], definition_suffix),
                p['type_format'] or '',
                '{}'.format(p['type_properties']) if p['type_properties'] else '',
                p['description']
            ))

                }}
    {% endfor %}

{% elif schema.all_of %}

{{ doc.get_type_description(schema.schema_id, definition_suffix) }}

{% else %}

{{ 'Any object ({})' }}

{% endif %}

{% if inline %}
    {% set _ = exists_schema.append(schema.schema_id) %}
{% endif %}

{% for schema_id in schema.nested_schemas %}
    {% set schema = doc.schemas.get(schema_id) %}
    {% if not schema.is_array %}
        {% if (not inline and schema.is_inline) or (inline and schema_id not in exists_schema) %}
            {% set schema_header = '**{} schema:**'.format(schema.name) %}

{% include "schema.rst"%}

        {% endif %}
    {% endif %}
{% endfor %}
