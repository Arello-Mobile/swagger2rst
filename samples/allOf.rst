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


**201**
^^^^^^^

Redefined create method

  
**Response Schema:**

 :ref:`AnswerModel <d_74b96a00174cffc078641e1f8c9fbb40>` extended :ref:`inline <i_d766acd89aec6b99c80c1b79b5a38a37>`


**Inline schema:**

 .. _i_d766acd89aec6b99c80c1b79b5a38a37:


.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        pdf_url | No | string |  |  |  
        guid1 | Yes | string |  |  |  
        favorites1 | Yes | array of string |  |  | custom answer Description 
        record_id | Yes | integer |  |  |  
        phrase_id | Yes | integer |  |  |  
        recording | Yes | string |  |  |  





**Example:**

.. code-block:: javascript

    {
        "phrase_id": 1, 
        "favorites1": [
            "somestring"
        ], 
        "guid1": "somestring", 
        "pdf_url": "somestring", 
        "recording": "somestring", 
        "record_id": 1
    }



**200**
^^^^^^^

Redefined update method

  
**Response Schema:**

 :ref:`RecordingSerializer <d_e408f13b0c465e8b895d79e7a4a4971c>` extended :ref:`inline <i_d766acd89aec6b99c80c1b79b5a38a37>`


**Inline schema:**

 .. _i_d766acd89aec6b99c80c1b79b5a38a37:


.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        pdf_url | No | string |  |  |  
        guid1 | Yes | string |  |  |  
        favorites1 | Yes | array of string |  |  | custom answer Description 
        record_id | Yes | integer |  |  |  
        phrase_id | Yes | integer |  |  |  
        recording | Yes | string |  |  |  





**Example:**

.. code-block:: javascript

    {
        "phrase_id": 1, 
        "favorites1": [
            "somestring"
        ], 
        "guid1": "somestring", 
        "pdf_url": "somestring", 
        "recording": "somestring", 
        "record_id": 1
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




