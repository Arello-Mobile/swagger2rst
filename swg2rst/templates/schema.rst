{% if schema_link or inline %}

.. _{{ '{}{}'.format(schema.schema_id, definition_suffix) }}:

{% endif %}

{{ schema_header }}

{% if schema.type == 'array' %}

{{ doc.get_type_description(schema.item['type'], definition_suffix) }}

{% endif %}

{% if schema.properties %}

{{ doc.get_regular_properties(schema.schema_id, definition_suffix) }}

{% elif schema.all_of %}

{{ doc.get_type_description(schema.schema_id, definition_suffix) }}

{% else %}

{{ doc.get_additional_properties(schema.schema_id, definition_suffix) }}

{% endif %}

{% if inline %}
    {% set _ = exists_schema.append(schema.schema_id) %}
{% endif %}

{% for schema_id in schema.nested_schemas %}
    {% set schema = doc.schemas.get(schema_id) %}
    {% if not schema.is_array %}
        {% if (not inline and schema.is_inline) or (inline and schema_id not in exists_schema) %}
            {% set schema_header = '**{} schema:**'.format(schema.name.capitalize()) %}

{% include "schema.rst"%}

        {% endif %}
    {% endif %}
{% endfor %}
