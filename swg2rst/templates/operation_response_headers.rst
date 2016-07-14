{{ 'Headers:' }}

.. code-block:: javascript

                    {% for header in response.headers.values() %}
    {{ doc.exampilator.get_header_example(header)|json_dumps(indent=4)|indent }}
                    {% endfor %}
