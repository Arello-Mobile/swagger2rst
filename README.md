# Swagger to .rst Converter

[![Build Status](https://travis-ci.org/Arello-Mobile/swagger2rst.svg?branch=master)](https://travis-ci.org/Arello-Mobile/swagger2rst)

## Install
```bash
pip install swagger2rst
```

## Usage examples
Command - ``swg2rst``

Required arguments:
- ``path`` - path to a swagger file ("json" or "yaml")
- ``--format (-f)`` - output file format. Currenty only "rst" is supported (required)

Options:
- ``--output (-o)`` - output filename (default: stdout)
- ``--template (-t)`` - custom template file path (default: templates/basic.<format>)
- ``--examples(-e)`` - custom examples definitions file path ("json" or "yaml")
- ``--inline (-i)`` - put schema definitions in paths, otherwise in a separate ``Data Structures`` section

Example:
```bash
> swg2rst samples/swagger.json -f rst -o /home/user/rst_docs/swagger.rst
> swg2rst samples/swagger.json -f rst -o /home/user/rst_docs/swagger.rst -e /home/user/examples.yaml
> cat docs/swagger.json | swg2rst -f rst -t templates/custom.rst | grep /api
```

## Additional enhancements
To convert GFM descriptions into _restructuredText_ install ``pandoc`` and use custom Jinja filter ``md2rst``

```bash
> sudo apt-get install pandoc
> pip install pypandoc
```

```python
{{ doc.info['description']|md2rst }}
```

## Custom Examples
Custom examples are described in **json** or **yaml**. See ``samples`` directory.

### Elements

#### ``array_items_count``
Number of elements in all arrays. Set from 1 to 5. Default: 2.

#### ``definitions``
Bind fields to examples by definition schemas.
Key is a definition reference path, value is an object (key is a field name and value is an example):

``json``
```json
{
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
}
```

``yaml``
```yaml
definitions:
    '#/definitions/Media':
        likes.count: 10
        likes.data.user_name: liked_user
        user.user_name: my_login
    '#/definitions/MiniProfile':
        user_name: some_login
        full_name: John Smith
```


#### ``paths``
Bind operation fields to examples by path.
Should define path, method, section (parameters or responses) and field name

``json``
```json
{
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
}
```

``yaml``
```yaml
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
```

#### ``types``
Define examples for primitive types.

Supported types:
- string
- date
- date-time
- number
- integer
- boolean

``json``
```json
{
    "types": {
        "string": "value",
        "date": "2000-12-01",
        "date-time": "2000-12-01T12:00:00.000Z",
        "number": 1.2,
        "integer": 5,
        "boolean": false
    }
}
```

``yaml``
```yaml
types:
    string: value
    date: '2000-12-01'
    date-time: '2000-12-01T12:00:00.000Z'
    number: 1.2
    integer: 5
    boolean: false
```

## Examples priorities
If a field has several examples, the following priority rules apply
1. Example from operation.
2. Example from definitions.
    If a schema has nested schemas, the priority is given to an example from a most descriptive.
    E.g.: ``Media`` has nested schema ``MiniProfile``.  For ``user_name`` in ``likes``
    in ``Media`` an example will be taken from ``#/definitions/Media/likes.data.user_name`` rather
    than from ``#/definitions/MiniProfile/user_name``.
3. Example from primitive types.
