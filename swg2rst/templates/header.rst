{{ '{title} {version}'.format(**doc.info)|header(1) }}

.. toctree::
    :maxdepth: 3

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

{% if doc.schemes %}
    {% for scheme in doc.schemes %}
{{ '{}://{}{}'.format(scheme, doc.host, doc.base_path) }}
    {% endfor %}
{% else %}
{{ 'http://{}{}'.format(doc.host, doc.base_path) }}
{% endif %}
{% endif -%}
