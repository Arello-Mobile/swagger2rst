
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
- ``--template (-t)`` - path to custom template file (default: templates/basic.<format>)

Example:

.. code-block:: bash

    swg2rst samples/swagger.json -f rst -d /home/user/rst_docs/
    cat docs/swagger.json | swg2rst -f rst -t templates/custom.rst | grep /api


Optional improvements
=====================

For converting GFM descriptions to restructuredText, install ``pandoc`` and use custom Jinja filter ``md2rst``

.. code-block:: bash

    sudo apt-get install pandoc
    pip install pypandoc


.. code-block:: django

    {{ doc.info['description']|md2rst }}


SWAGGER Structure
=================

.. automodule:: swg2rst.swagger
    :members:
    :undoc-members:
