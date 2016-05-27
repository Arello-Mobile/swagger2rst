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

Redefined update method

 
**Response Schema:**

:ref:`RecordingSerializer <d_e408f13b0c465e8b895d79e7a4a4971cquestionnaireget_api_v1_questionnaire_get>` extended :ref:`inline <i_d766acd89aec6b99c80c1b79b5a38a37questionnaireget_api_v1_questionnaire_get>`

**Recordingserializer schema:**


.. _d_e408f13b0c465e8b895d79e7a4a4971cquestionnaireget_api_v1_questionnaire_get:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        phrase_id | Yes | integer |  |  |  
        record_id | Yes | integer |  |  |  
        recording | Yes | string |  |  |  


**Inline schema:**


.. _i_d766acd89aec6b99c80c1b79b5a38a37questionnaireget_api_v1_questionnaire_get:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        favorites1 | Yes | array of string |  |  | custom answer Description 
        guid1 | Yes | string |  |  |  
        pdf_url | No | string |  |  |  
        phrase_id | Yes | integer |  |  |  
        record_id | Yes | integer |  |  |  
        recording | Yes | string |  |  |  




**Example:**

.. code-block:: javascript

    {
        "favorites1": [
            "value",
            "value",
            "value"
        ],
        "guid1": "value",
        "pdf_url": "value",
        "phrase_id": 5,
        "record_id": 5,
        "recording": "value"
    }

**201**
^^^^^^^

Redefined create method

 
**Response Schema:**

:ref:`AnswerModel <d_74b96a00174cffc078641e1f8c9fbb40questionnaireget_api_v1_questionnaire_get>` extended :ref:`inline <i_d766acd89aec6b99c80c1b79b5a38a37questionnaireget_api_v1_questionnaire_get>`

**Answermodel schema:**


.. _d_74b96a00174cffc078641e1f8c9fbb40questionnaireget_api_v1_questionnaire_get:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        favorites1 | Yes | array of string |  |  | custom answer Description 
        guid1 | Yes | string |  |  |  




**Inline schema:**


.. _i_d766acd89aec6b99c80c1b79b5a38a37questionnaireget_api_v1_questionnaire_get:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        favorites1 | Yes | array of string |  |  | custom answer Description 
        guid1 | Yes | string |  |  |  
        pdf_url | No | string |  |  |  
        phrase_id | Yes | integer |  |  |  
        record_id | Yes | integer |  |  |  
        recording | Yes | string |  |  |  




**Example:**

.. code-block:: javascript

    {
        "favorites1": [
            "value",
            "value",
            "value"
        ],
        "guid1": "value",
        "pdf_url": "value",
        "phrase_id": 5,
        "record_id": 5,
        "recording": "value"
    }

  

  
  
