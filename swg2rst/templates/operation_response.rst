{{ '**{}**'.format(code)|header(5) }}

{{ response.description }}

{% if doc.schemas.contains(response.type) %}
    {% set schema = doc.schemas.get(response.type) %}
    {% if not schema.is_inline and inline %}
        {% set schema_header = '**{} schema:**\n'.format(schema.name.capitalize()) %}
    {% else %}
        {% set schema_header = '**Response Schema:**' %}
    {% endif %}
    {% set exists_schema = [] %}

    {% if not schema.is_inline or schema.is_array %}
Type: {{ doc.get_type_description(response.type, definition_suffix) }}

    {% endif %}
    {% if schema.is_inline or inline %}
        {% set definition = inline %}
        {%- include "schema.rst" %}

    {% endif %}
    {% if response.headers %}
        {%- include "operation_response_headers.rst" %}

    {% endif %}
    {%- include "operation_response_example.rst" %}

{% endif %}
