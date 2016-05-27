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

.. _i_adc5092c0495e31ec8c2b1e3d5616118questionnaireget_api_v1_questionnaire_get:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        response | Yes | :ref:`response <i_05aab4aaa38ed83e6383d8b120b695c5questionnaireget_api_v1_questionnaire_get>` |  |  |  
        status | Yes | integer |  | {'default': 200} |  


**Response schema:**


.. _i_05aab4aaa38ed83e6383d8b120b695c5questionnaireget_api_v1_questionnaire_get:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        answers | Yes | :ref:`answers <i_d03ea09112dff29f2c95309ef502fed9questionnaireget_api_v1_questionnaire_get>` |  |  |  
        questions | Yes | :ref:`questions <i_539115816613abf68d313ca0586de7e7questionnaireget_api_v1_questionnaire_get>` |  |  |  
        requests1 | No | :ref:`requests1 <i_35b332450e99af3d9e0eb0ff232dea8aquestionnaireget_api_v1_questionnaire_get>` |  |  |  
        requests2 | No | :ref:`requests2 <i_fe6f6ae5256e52bfb028466852b07893questionnaireget_api_v1_questionnaire_get>` |  |  |  
        sections | Yes | :ref:`sections <i_2bc22d0da58d3c1817cb53aa6d18e9f7questionnaireget_api_v1_questionnaire_get>` |  |  |  
        sentenses | No | :ref:`sentenses <i_b246b2a0877e8d811e8f59c29810deb1questionnaireget_api_v1_questionnaire_get>` |  |  |  


**Answers schema:**


.. _i_d03ea09112dff29f2c95309ef502fed9questionnaireget_api_v1_questionnaire_get:

Map of {"key":":ref:`AnswerModel <d_74b96a00174cffc078641e1f8c9fbb40questionnaireget_api_v1_questionnaire_get>`"}



**Answermodel schema:**


.. _d_74b96a00174cffc078641e1f8c9fbb40questionnaireget_api_v1_questionnaire_get:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        favorites1 | Yes | array of string |  |  | custom answer Description 
        guid1 | Yes | string |  |  |  




**Questions schema:**


.. _i_539115816613abf68d313ca0586de7e7questionnaireget_api_v1_questionnaire_get:

Map of {"key":":ref:`questions-mapped <m_e848bde974d09e8a4a002fabe86c1c38questionnaireget_api_v1_questionnaire_get>`"}

.. _m_e848bde974d09e8a4a002fabe86c1c38questionnaireget_api_v1_questionnaire_get:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        proper1 | No | string |  |  |  
        proper2 | No | string |  |  |  


**Questions-mapped schema:**


.. _m_e848bde974d09e8a4a002fabe86c1c38questionnaireget_api_v1_questionnaire_get:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        proper1 | No | string |  |  |  
        proper2 | No | string |  |  |  


**Requests1 schema:**


.. _i_35b332450e99af3d9e0eb0ff232dea8aquestionnaireget_api_v1_questionnaire_get:

Map of {"key":"array of :ref:`requests1-mapped <i_cc81fedcd46afeecd14ab39aef491776questionnaireget_api_v1_questionnaire_get>`"}

.. _i_cc81fedcd46afeecd14ab39aef491776questionnaireget_api_v1_questionnaire_get:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        arr_prop1 | No | string |  |  |  
        arr_prop2 | No | integer |  |  |  




**Requests1-mapped schema:**

another descr to search it

.. _i_cc81fedcd46afeecd14ab39aef491776questionnaireget_api_v1_questionnaire_get:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        arr_prop1 | No | string |  |  |  
        arr_prop2 | No | integer |  |  |  


**Requests2 schema:**


.. _i_fe6f6ae5256e52bfb028466852b07893questionnaireget_api_v1_questionnaire_get:

Map of {"key":"array of :ref:`RecordingSerializer <d_e408f13b0c465e8b895d79e7a4a4971cquestionnaireget_api_v1_questionnaire_get>`"}





**Recordingserializer schema:**


.. _d_e408f13b0c465e8b895d79e7a4a4971cquestionnaireget_api_v1_questionnaire_get:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        phrase_id | Yes | integer |  |  |  
        record_id | Yes | integer |  |  |  
        recording | Yes | string |  |  |  


**Sections schema:**


.. _i_2bc22d0da58d3c1817cb53aa6d18e9f7questionnaireget_api_v1_questionnaire_get:

Map of {"key":"array of string"}





**Sentenses schema:**


.. _i_b246b2a0877e8d811e8f59c29810deb1questionnaireget_api_v1_questionnaire_get:

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

  

  
  
