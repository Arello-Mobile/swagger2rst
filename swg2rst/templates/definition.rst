{% if not inline %}
{{ "Data Structures"|header(2) }}

    {% set schema_link = True %}

    {% for schema in doc.schemas.get_schemas(['definition']) -%}
        {% set schema_header = '{} Model Structure'.format(schema.name)|header(3) %}
        {% set basic = False %}
        {% set definition = True %}
        {% set exists_schema = [] %}

        {%- include "schema.rst" -%}

    {%- endfor %}
{% endif %}
