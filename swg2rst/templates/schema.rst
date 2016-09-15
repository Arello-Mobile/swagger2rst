{% set _ = exists_schema.append(schema_id) %}
{% if not schema.is_array %}
.. _{{ schema.schema_id }}{{ definition_suffix }}:

{{ schema_header }}

    {% if schema.description %}
        {{- schema.description }}

    {% endif %}
    {% if schema.items %}
        {{- doc.get_type_description(schema.item['type'], definition_suffix) }}

    {% elif schema.properties %}
        {{- doc.get_regular_properties(schema.schema_id, definition_suffix, definition=definition) }}

    {% elif schema.all_of %}
        {{- doc.get_type_description(schema.schema_id, definition_suffix) }}

    {% else %}
        {{- doc.get_additional_properties(schema.schema_id, definition_suffix) }}

    {% endif %}
{% endif %}
{% for schema_id in doc.sorted(schema.nested_schemas) if schema_id not in exists_schema %}
    {% set schema = doc.schemas.get(schema_id) %}
    {% if schema.is_inline or inline %}
        {% set schema_header = '**{} schema:**\n'.format(schema.name.capitalize()) %}
        {%- include "schema.rst" %}
    {% endif %}
{% endfor %}
