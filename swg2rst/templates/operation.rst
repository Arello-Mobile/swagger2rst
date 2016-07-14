{% for tag, operations in doc.tags|dictsort %}

{{ tag|upper|header(2) }}

    {% if doc.tag_descriptions and tag in doc.tag_descriptions %}

{{ doc.tag_descriptions[tag]['description'] }}

        {% if doc.tag_descriptions[tag]['externalDocs'] %}

{{ doc.tag_descriptions[tag]['externalDocs'] }}

        {% endif %}

    {% endif %}

    {% for operation in doc.sorted(operations) %}
{% set definition_suffix = (tag + operation.operation_id) if inline else '' %}


{{ '{} ``{}``'.format(operation.method.upper(), operation.path)|header(3) }}

        {% if operation.deprecated %}

.. raw:: html

    This operation marked as <span style="color: red">DEPRECATED</span>!!!

        {% endif %}

        {% if operation.summary %}
{{ 'Summary'|header(4) }}

{{ operation.summary }}
        {% endif %}

        {% if operation.description %}
{{ 'Description'|header(4) }}

.. raw:: html

    {{ operation.description }}
        {% endif %}

        {% set parameters = operation.get_parameters_by_location(excludes=['header', 'body']) %}
        {% if  parameters %}
{{ 'Parameters'|header(4) }}

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

            {% for p in parameters %}
        {{
            ' | '.join((
            p.name,
            p.location_in,
            'Yes' if p.required else 'No',
            doc.get_type_description(p.type, definition_suffix),
            p.type_format or '',
            '{}'.format(p.properties|json_dumps) if p.properties else '',
            p.description|replace('\n', ' ')
              ))
              }}
            {% endfor %}

        {% endif %}

{{ 'Request'|header(4) }}

        {% set headers = operation.get_parameters_by_location(['header']) %}
        {% if headers %}

{{ 'Headers'|header(5) }}

.. code-block:: javascript

            {% for header in headers %}
                {% if header.properties %}
    {{ '{}: {}'.format(header.name, header.properties['default']) }}
                {% else %}
    {{ '{}: {}'.format(header.name, header.description) }}
                {% endif %}
            {% endfor %}

        {% endif %}

        {% if operation.body %}

            {% set schema = operation.body %}
            {% set schema_header = 'Body'|header(5) %}
            {% set exists_schema = [] %}
            {% set definition = True %}

            {%- include "schema.rst" -%}

.. code-block:: javascript

    {{ doc.exampilator.get_body_example(operation)|json_dumps(indent=4)|indent }}

        {% endif %}

        {%- include 'operation_responses.rst' %}


        {% if operation.security %}
            {%- include 'operation_security.rst' %}
        {% endif %}
    {% endfor %}  {# end operations #}
{% endfor -%}  {# end tags #}
