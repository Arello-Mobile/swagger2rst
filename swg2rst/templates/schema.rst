{% if not (internal_call and schema.is_array) -%}
{{- schema_header }}
    {% if schema.description %}
{{ schema.description }}
    {% endif %}

    {% if schema.items -%}
{{- doc.get_type_description(schema.item['type'], definition_suffix) -}}
    {%- elif schema.properties -%}
{{- doc.get_regular_properties(schema.schema_id, definition_suffix, definition=definition) -}}
    {%- elif schema.all_of -%}
{{- doc.get_type_description(schema.schema_id, definition_suffix) -}}
    {%- else -%}
{{- doc.get_additional_properties(schema.schema_id, definition_suffix) -}}
    {%- endif %}

{%- endif %}


{% for schema_id in doc.sorted(schema.nested_schemas) -%}
    {% set schema = doc.schemas.get(schema_id) %}
    {% set internal_call = True %}
    {% set schema_header = '**{} schema:**\n'.format(schema.name.capitalize()) %}
    {% if schema.is_inline and not inline %}

        {%- include "schema.rst" -%}

    {% elif inline %}
        {% set definition = True %}

        {%- include "schema.rst" -%}

        {% set definition = False %}
    {% endif %}
    {% set internal_call = False %}    
{%- endfor %}
