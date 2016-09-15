{% if doc.security_definitions %}

{{ 'Security'|header(2) }}

    {% for _, security in doc.sorted(doc.security_definitions) %}

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
