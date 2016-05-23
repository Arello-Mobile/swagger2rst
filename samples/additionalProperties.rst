API title 0.0.1
===============

.. toctree::
    :maxdepth: 3





Base URL
~~~~~~~~

http:///



QUESTIONNAIRE
~~~~~~~~~~~~~



GET ``/api/v1/questionnaire/get/``
----------------------------------


Summary
+++++++

Return Recording Questionnaire



Request
+++++++



Responses
+++++++++


**200**
^^^^^^^

Recording Questionnaire


 
**Response Schema:**

.. _i_ee09233c5ee96677fa92701bed91e9ae:


.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        status | Yes | integer |  | {'default': 200} |
        response | Yes | :ref:`response <i_a4c260362900d352b86cc64a01d890b3>` |  |  |






**Response schema:**

.. _i_a4c260362900d352b86cc64a01d890b3:


.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        sentenses | No | :ref:`sentenses <i_9e98b7141727d191f77df8492cb7add6>` |  |  |
        requests2 | No | :ref:`requests2 <i_eb4a50f659b30fecba9180ab7d26fa59>` |  |  |
        answers | Yes | :ref:`answers <i_8453d26e777ff18163fc98b061d14c2d>` |  |  |
        requests1 | No | :ref:`requests1 <i_7e30217bf9065318261849e6259c1493>` |  |  |
        questions | Yes | :ref:`questions <i_539115816613abf68d313ca0586de7e7>` |  |  |
        sections | Yes | :ref:`sections <i_c13559922a66dad4f7d7523cf83e1c0c>` |  |  |






**Requests2 schema:**

.. _i_eb4a50f659b30fecba9180ab7d26fa59:


Map of {"string":"array of :ref:`RecordingSerializer <d_e408f13b0c465e8b895d79e7a4a4971c>`"}







**Answers schema:**

.. _i_8453d26e777ff18163fc98b061d14c2d:


Map of {"string":":ref:`AnswerModel <d_74b96a00174cffc078641e1f8c9fbb40>`"}







**Sentenses schema:**

.. _i_9e98b7141727d191f77df8492cb7add6:


Map of {"string":"string"}





**Requests1 schema:**

.. _i_7e30217bf9065318261849e6259c1493:


Map of {"string":"array of :ref:`requests1-mapped <i_6c81316903d873831f0ba9c50df62929>`"}

.. _i_6c81316903d873831f0ba9c50df62929:


.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        arr_prop1 | No | string |  |  |
        arr_prop2 | No | integer |  |  |






**Sections schema:**

.. _i_c13559922a66dad4f7d7523cf83e1c0c:


Map of {"string":"array of string"}







**Questions schema:**

.. _i_539115816613abf68d313ca0586de7e7:


Map of {"string":":ref:`questions-mapped <m_e848bde974d09e8a4a002fabe86c1c38>`"}

.. _m_e848bde974d09e8a4a002fabe86c1c38:


.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        proper1 | No | string |  |  |
        proper2 | No | string |  |  |






**Example:**

.. code-block:: javascript

    {
        "status": 200,
        "response": {
            "sentenses": {},
            "requests2": {},
            "requests1": {},
            "answers": {},
            "questions": {},
            "sections": {}
        }
    }






Data Structures
~~~~~~~~~~~~~~~



AnswerModel Model Structure
---------------------------

.. _d_74b96a00174cffc078641e1f8c9fbb40:


.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        guid1 | Yes | string |  |  |
        favorites1 | Yes | array of string |  |  | custom answer Description








RecordingSerializer Model Structure
-----------------------------------
 
.. _d_e408f13b0c465e8b895d79e7a4a4971c:


.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        record_id | Yes | integer |  |  |  
        phrase_id | Yes | integer |  |  |  
        recording | Yes | string |  |  |  






