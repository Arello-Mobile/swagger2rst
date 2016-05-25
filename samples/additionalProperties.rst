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


.. _i_809a6c5ceacaf76e237dde71041d3334:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        response | Yes | :ref:`response <i_6d881509c9268154c419701de606afe1>` |  |  |  
        status | Yes | integer |  | {'default': 200} |  


**Response schema:**


.. _i_6d881509c9268154c419701de606afe1:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        answers | Yes | :ref:`answers <i_8453d26e777ff18163fc98b061d14c2d>` |  |  |  
        questions | Yes | :ref:`questions <i_c4530b74317b8351e6d5acabf8b295c1>` |  |  |  
        requests1 | No | :ref:`requests1 <i_6efdee9f24e51ede091d15c18eeeea78>` |  |  |  
        requests2 | No | :ref:`requests2 <i_0c22b0335f674aae2b11f9b9ff45e94b>` |  |  |  
        sections | Yes | :ref:`sections <i_8448f5be0db72fe109da093eb8fc3a60>` |  |  |  
        sentenses | No | :ref:`sentenses <i_8059a72f9a14ad218776f978bd70cb5f>` |  |  |  


**Answers schema:**


.. _i_8453d26e777ff18163fc98b061d14c2d:

Map of {"key":":ref:`AnswerModel <d_74b96a00174cffc078641e1f8c9fbb40>`"}



**Questions schema:**


.. _i_c4530b74317b8351e6d5acabf8b295c1:

Map of {"key":":ref:`questions-mapped <m_9ac9356799680f72839e6d91ab89d34f>`"}

.. _m_9ac9356799680f72839e6d91ab89d34f:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        proper1 | No | string |  |  |  
        proper2 | No | string |  |  |  


**Requests1 schema:**


.. _i_6efdee9f24e51ede091d15c18eeeea78:

Map of {"key":"array of :ref:`requests1-mapped <i_0c8fd7118f61fe6ea6f27d1803fcb046>`"}

.. _i_0c8fd7118f61fe6ea6f27d1803fcb046:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        arr_prop1 | No | string |  |  |  
        arr_prop2 | No | integer |  |  |  


**Requests2 schema:**


.. _i_0c22b0335f674aae2b11f9b9ff45e94b:

Map of {"key":"array of :ref:`RecordingSerializer <d_e408f13b0c465e8b895d79e7a4a4971c>`"}



**Sections schema:**


.. _i_8448f5be0db72fe109da093eb8fc3a60:

Map of {"key":"array of string"}



**Sentenses schema:**


.. _i_8059a72f9a14ad218776f978bd70cb5f:

Map of {"key":"string"}



**Example:**

.. code-block:: javascript

    {
        "response": {
            "answers": {},
            "questions": {},
            "requests1": {},
            "requests2": {},
            "sections": {},
            "sentenses": {}
        },
        "status": 200
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

        favorites1 | Yes | array of string |  |  | custom answer Description 
        guid1 | Yes | string |  |  |  




RecordingSerializer Model Structure
-----------------------------------


.. _d_e408f13b0c465e8b895d79e7a4a4971c:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        phrase_id | Yes | integer |  |  |  
        record_id | Yes | integer |  |  |  
        recording | Yes | string |  |  |  
