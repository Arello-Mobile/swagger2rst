{% set collapsible = True %}
{{ '{title} {version}'.format(**doc.info)|header(1) }}

.. toctree::
    :maxdepth: 3

    {{ filename }}

{% if doc.info['description'] %}

{{ 'Description'|header(2) }}

{{ doc.info['description']|md2rst }}

{% endif %}

{% if doc.info['contact'] %}

{{ 'Contact Information'|header(2) }}

    {% if 'name' in doc.info['contact'] %}

{{ doc.info['contact']['name'] }}

    {% endif %}

    {% if 'email' in doc.info['contact'] %}

{{ doc.info['contact']['email'] }}

    {% endif %}

    {% if 'url' in doc.info['contact'] %}

{{ doc.info['contact']['url'] }}

    {% endif %}

{% endif %}

{% if doc.info['license'] %}

{{ 'License'|header(2) }}

    {% if 'url' in doc.info['license'] %}

{{ '`{name} <{url}>`_'.format(**doc.info['license']) }}

    {% else %}

{{ doc.info['license']['name'] }}

    {% endif %}

{% endif %}

{% if doc.host or doc.base_path %}

{{ 'Base URL'|header(2) }}

{{ 'http://{}{}'.format(doc.host, doc.base_path) }}

{% endif -%}

{% if doc.security_definitions %}

{{ 'Security'|header(2) }}

    {% for security in doc.security_definitions.values() %}

.. _{{ 'securities_{}'.format(security.name) }}:

{{ '{} ({})'.format(security.name, security.type_name)|header(3) }}

        {% if security.description %}

*{{ security.description }}*

        {% endif %}

        {% if security.type == 'oauth2' %}

{{ '**Flow:** {}'.format(security.flow) }}

            {% if security.auth_url %}

{{ '**Authorization URL:** {}'.format(security.auth_url) }}

            {% endif %}

            {% if security.token_url %}

{{ '**Token URL:** {}'.format(security.token_url) }}

            {% endif %}

{{ 'Scopes'|header(4) }}

.. csv-table::
    :header: "Scope", "Description"
    :widths: 10, 50

            {% for scope, description in security.scopes|dictsort %}
        {{ scope }} , "{{ description|replace('\n', ' ')|trim }}"
            {% endfor %}

        {% elif security.type == 'apiKey' %}

{{ '**Name:** {}'.format(security.param_name) }}

{{ '**Located in:** {}'.format(security.location_in) }}

        {% endif %}

    {% endfor %}

{% endif %}

{% for tag, operations in doc.tags|dictsort %}

{{ tag|upper|header(2) }}

    {% if doc.tag_descriptions and tag in doc.tag_descriptions %}

{{ doc.tag_descriptions[tag]['description'] }}

        {% if doc.tag_descriptions[tag]['externalDocs'] %}

{{ doc.tag_descriptions[tag]['externalDocs'] }}

        {% endif %}

    {% endif %}

    {% for operation in operations %}
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
    {{ '{}: {}'.format(header.name, header.properties['default']) }}
            {% endfor %}

        {% endif %}

        {% if operation.body %}

            {% set schema = operation.body %}
            {% set schema_header = 'Body'|header(5) %}
            {% set schema_link = False %}
            {% set exists_schema = [] %}

{% include "schema.rst" %}

            {% set schema_link = True %}

.. code-block:: javascript

    {{ doc.exampilator.get_body_example(operation)|json_dumps(indent=4)|indent }}

        {% endif %}

{{ 'Responses'|header(4) }}

        {% for code, response in operation.responses.items() %}

{{ '**{}**'.format(code)|header(5) }}

{{ response.description }}

            {% if doc.schemas.contains(response.type) %}
                {% set schema = doc.schemas.get(response.type) %}
                {% if not schema.is_inline or schema.is_array %}

Type: {{ doc.get_type_description(response.type) }}

                {% else %}
                    {% set schema_header = '**Response Schema:**' %}
                    {% set exists_schema = [] %}

{% include "schema.rst" %}
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

        {% endfor %}  {# end responses #}

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

{% if not inline %}
{{ "Data Structures"|header(2) }}

    {% set schema_link = True %}

    {% for schema in doc.schemas.get_schemas(['definition']) %}
        {% set schema_header = '{} Model Structure'.format(schema.name)|header(3) %}

{% include "schema.rst" %}

    {% endfor %}
{% endif %}
