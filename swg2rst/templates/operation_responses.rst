{{ 'Responses'|header(4) }}

{% for code, response in doc.sorted(operation.responses) %}
    {%- include 'operation_response.rst' %}

{% endfor %}
