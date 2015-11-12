
Swagger to .rst Converter
=========================

.. toctree::
    :maxdepth: 2

    doc

Install
=======

.. code-block:: bash

    pip install swagger2rst

Use Command
===========
Command - ``swg2rst``

Positional arguments:

- ``path`` - path to swagger file - "json" or "yaml"

Options:

- ``--format(-f)`` - format output doc file - "rst" (required)
- ``--destination-path (-d)`` - path to folder for saving files
- ``--template (-t)`` - path to custom template fisle (default: templates/basic.<format>)
- ``--examples (-e)`` - path to custom examples file - "json" or "yaml"
- ``--inline (-i)`` - output schema definitions locally in paths, otherwise in isolated section ``Data Structures``

Example:

.. code-block:: bash

    swg2rst samples/swagger.json -f rst -d /home/user/rst_docs/
    swg2rst samples/swagger.json -f rst -d /home/user/rst_docs/ -e /home/user/examples.yaml
    cat docs/swagger.json | swg2rst -f rst -t templates/custom.rst | grep /api


Optional improvements
=====================

For converting GFM descriptions to restructuredText, install ``pandoc`` and use custom Jinja filter ``md2rst``

.. code-block:: bash

    sudo apt-get install pandoc
    pip install pypandoc


.. code-block:: django

    {{ doc.info['description']|md2rst }}


Custom Examples
===============

Custom examples define by format json or yaml. Samples locate in folder ``samples``.

Elements
~~~~~~~~

``array_items_count``
---------------------

Declares count of elements in all arrays. Set value from 1 to 5. Default: 2.

``definitions``
---------------

Declares examples for fields in definitions schemas.
Key is definition reference path, value is object, where key is field name and value is example:

``json``

.. code-block:: javascript

    "definitions": {
        "#/definitions/Media": {
            "likes.count": 10,
            "likes.data.user_name": "liked_user",
            "user.user_name": "my_login"
        },
        "#/definitions/MiniProfile": {
            "user_name": "some_login",
            "full_name": "John Smith"
        }
    }


``yaml``

.. code-block:: python

    definitions:
        '#/definitions/Media':
            likes.count: 10
            likes.data.user_name: liked_user
            user.user_name: my_login
        '#/definitions/MiniProfile':
            user_name: some_login
            full_name: John Smith


``paths``
---------

Declares examples for fields in operations.
Necessary set path, method, section (parameters or responses) and field name

``json``

.. code-block:: javascript

    "paths": {
        "/users/{user-id}/relationship": {
            "post": {
                "parameters": {
                    "action": "approve"
                },
                "responses": {
                    "200.data": {
                        "profile_picture": "picture",
                        "full_name": "Kevin Jones",
                        "id": 10,
                        "user_name": "kevin"
                    }
                }
            }
        }
    }


``yaml``

.. code-block:: python

    paths:
        /users/{user-id}/relationship:
            post:
                parameters:
                    action: approve
                responses:
                    200.data.profile_picture: picture
                    200.data.full_name: Kevin Jones
                    200.data.id: 10
                    200.data.user_name: kevin


``types``
---------

Declare examples for primitive types.
Available types:

- string
- date
- date-time
- number
- integer
- boolean

``json``

.. code-block:: javascript

    "types": {
        "string": "value",
        "date": "2000-12-01",
        "date-time": "2000-12-01T12:00:00.000Z",
        "number": 1.2,
        "integer": 5,
        "boolean": false
    }


``yaml``

.. code-block:: python

    types:
        string: value
        date: '2000-12-01'
        date-time: '2000-12-01T12:00:00.000Z'
        number: 1.2
        integer: 5
        boolean: false


Example Priorities
~~~~~~~~~~~~~~~~~~

If field is matched to several examples, following priority rules apply

1. Example from operation
2. Example from definitions.

    If schema has nested schemas, priority is an example of description with the maximum,

    For example definition ``Media`` has nested schema ``MiniProfile``.
    For field ``user_name`` in object ``likes`` for ``Media`` instance priority example is
    ``#/definitions/Media/likes.data.user_name`` rather than ``#/definitions/MiniProfile/user_name``

3. Example from primitive types


SWAGGER Structure
=================

.. automodule:: swg2rst.swagger
    :members:
    :undoc-members:
