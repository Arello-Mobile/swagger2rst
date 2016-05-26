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

.. _i_b60304d1e15eccd74abac85655cf859a:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        response | Yes | :ref:`response <i_2c8baa718514018f8bc0b15b423bc7b0>` |  |  |  
        status | Yes | integer |  | {'default': 200} |  


**Response schema:**

.. _i_2c8baa718514018f8bc0b15b423bc7b0:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        answers | Yes | :ref:`answers <i_8453d26e777ff18163fc98b061d14c2d>` |  |  |  
        questions | Yes | :ref:`questions <i_c4530b74317b8351e6d5acabf8b295c1>` |  |  |  
        requests1 | No | :ref:`requests1 <i_62f432528056b6f32c9ea8bfe0276d1b>` |  |  |  
        requests2 | No | :ref:`requests2 <i_48aa77cca2f9cb3ebcb0afbba0e5eb9d>` |  |  |  
        sections | Yes | :ref:`sections <i_6e552287c5f0f7d46990033e84933f00>` |  |  |  
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

.. _i_62f432528056b6f32c9ea8bfe0276d1b:

Map of {"key":"array of :ref:`requests1-mapped <i_22992d629998ed1482233fed32b5f3e2>`"}

.. _i_22992d629998ed1482233fed32b5f3e2:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        arr_prop1 | No | string |  |  |  
        arr_prop2 | No | integer |  |  |  


**Requests2 schema:**

.. _i_48aa77cca2f9cb3ebcb0afbba0e5eb9d:

Map of {"key":"array of :ref:`RecordingSerializer <d_e408f13b0c465e8b895d79e7a4a4971c>`"}



**Sections schema:**

.. _i_6e552287c5f0f7d46990033e84933f00:

Map of {"key":"array of string"}



**Sentenses schema:**

.. _i_8059a72f9a14ad218776f978bd70cb5f:

Map of {"key":"string"}



**Example:**

.. code-block:: javascript

    {
        "response": {
            "answers": {
                "AnswerModel": {
                    "favorites1": [
                        "value",
                        "value",
                        "value"
                    ],
                    "guid1": "value"
                }
            },
            "questions": {
                "questions-mapped": {
                    "proper1": "value",
                    "proper2": "value"
                }
            },
            "requests1": {
                "requests1-mapped_array": [
                    {
                        "arr_prop1": "value",
                        "arr_prop2": 5
                    },
                    {
                        "arr_prop1": "value",
                        "arr_prop2": 5
                    },
                    {
                        "arr_prop1": "value",
                        "arr_prop2": 5
                    }
                ]
            },
            "requests2": {
                "requests2-mapped_array": [
                    {
                        "phrase_id": 5,
                        "record_id": 5,
                        "recording": "value"
                    },
                    {
                        "phrase_id": 5,
                        "record_id": 5,
                        "recording": "value"
                    },
                    {
                        "phrase_id": 5,
                        "record_id": 5,
                        "recording": "value"
                    }
                ]
            },
            "sections": {
                "sections-mapped_array": [
                    "value",
                    "value",
                    "value"
                ]
            },
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


