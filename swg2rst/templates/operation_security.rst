{{ 'Security'|header(4) }}

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

    {% for name, scopes in operation.security|dictsort %}
        {{ ':ref:`{name} <securities_{name}>`'.format(name=name) }}, "{{ ', '.join(scopes) }}"
    {% endfor %}
