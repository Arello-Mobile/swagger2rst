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
            {% set schema_link = False %}
            {% set exists_schema = [] %}
            {% set basic = False %}
            {% set definition = True %}

            {%- include "schema.rst" -%}

            {% set schema_link = True %}

.. code-block:: javascript

    {{ doc.exampilator.get_body_example(operation)|json_dumps(indent=4)|indent }}

        {% endif %}

{{ 'Responses'|header(4) }}

        {% for code, response in doc.sorted(operation.responses) -%}

{{ '**{}**'.format(code)|header(5) }}

{{ response.description }}

            {% if doc.schemas.contains(response.type) %}
                {% set schema = doc.schemas.get(response.type) %}
                {% set schema_header = '**Response Schema:**' %}
                {% set exists_schema = [] %}
                {% set basic = False %} {# used for recursion count #}

                {% if not schema.is_inline or schema.is_array %}
Type: {{ doc.get_type_description(response.type, definition_suffix) }}

                {% if inline %}
                    {% set temp_schema = doc.schemas.get(response.type) -%}
                    {{ '**{} schema:**\n'.format(temp_schema.name.capitalize()) }}
                    {% if schema.is_array %}
{{ doc.get_regular_properties(temp_schema.item['type'], definition_suffix, definition=True) }}
                    {% elif schema.properties %}
{{ doc.get_regular_properties(response.type, definition_suffix, definition=True) }}
                    {% else %}
{{ doc.get_additional_properties(schema.schema_id, definition_suffix) }}
                    {% endif %}
                {% endif %}
                {% else %}

{%- include "schema.rst" -%}

            {% endif %}

                {% if response.headers %}

{{ 'Headers:' }}

.. code-block:: javascript

                    {% for header in response.headers.values() %}
    {{ doc.exampilator.get_header_example(header)|json_dumps(indent=4)|indent }}
                    {% endfor %}

                {% endif %}

{{ '**Example:**' }}

.. code-block:: javascript

    {{ doc.exampilator.get_response_example(operation, response)|json_dumps(indent=4)|indent }}

            {% endif %}

        {%- endfor %}  {# end responses #}

        {% if operation.security %}

{{ 'Security'|header(4) }}

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

            {% for name, scopes in operation.security|dictsort %}
        {{ ':ref:`{name} <securities_{name}>`'.format(name=name) }}, "{{ ', '.join(scopes) }}"
            {% endfor %}

        {% endif %}

    {% endfor %}  {# end operations #}

{% endfor %}  {# end tags #}
