{% if not (internal_call and schema.is_array) -%}
{{- schema_header }}


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
    {# if (not inline and schema.is_inline) or (inline and schema_id not in exists_schema) #}
    {% if schema.is_inline %}
        {% set schema_header = '**{} schema:**'.format(schema.name.capitalize()) %}
        {% set internal_call = True %}

        {%- include "schema.rst" -%}

        {% set internal_call = False %}
    {% endif %}
{%- endfor %}
