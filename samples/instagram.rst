Instagram API v1
================

.. toctree::
    :maxdepth: 3


Description
~~~~~~~~~~~

The first version of the Instagram API is an exciting step forward towards
making it easier for users to have open access to their data. We created it
so that you can surface the amazing content Instagram users share every
second, in fun and innovative ways.


Build something great!


Once you've
[registered your client](http://instagram.com/developer/register/) it's easy
to start requesting data from Instagram.


All endpoints are only accessible via https and are located at
`api.instagram.com`. For instance: you can grab the most popular photos at
the moment by accessing the following URL with your client ID
(replace CLIENT-ID with your own):



  https://api.instagram.com/v1/media/popular?client_id=CLIENT-ID



You're best off using an access_token for the authenticated user for each
endpoint, though many endpoints don't require it.
In some cases an access_token will give you more access to information, and
in all cases, it means that you are operating under a per-access_token limit
vs. the same limit for your single client_id.




## Limits
Be nice. If you're sending too many requests too quickly, we'll send back a
`503` error code (server unavailable).
You are limited to 5000 requests per hour per `access_token` or `client_id`
overall. Practically, this means you should (when possible) authenticate
users so that limits are well outside the reach of a given user.


## Deleting Objects
We do our best to have all our URLs be
[RESTful](http://en.wikipedia.org/wiki/Representational_state_transfer).
Every endpoint (URL) may support one of four different http verbs. GET
requests fetch information about an object, POST requests create objects,
PUT requests update objects, and finally DELETE requests will delete
objects.


Since many old browsers don't support PUT or DELETE, we've made it easy to
fake PUTs and DELETEs. All you have to do is do a POST with _method=PUT or
_method=DELETE as a parameter and we will treat it as if you used PUT or
DELETE respectively.


## Structure


### The Envelope
Every response is contained by an envelope. That is, each response has a
predictable set of keys with which you can expect to interact:

json
{

    "meta": {

        "code": 200

    },

    "data": {

        ...

    },

    "pagination": {

        "next_url": "...",

        "next_max_id": "13872296"

    }

}




#### META
The meta key is used to communicate extra information about the response to
the developer. If all goes well, you'll only ever see a code key with value
200. However, sometimes things go wrong, and in that case you might see a
response like:

json
{

    "meta": {

        "error_type": "OAuthException",

        "code": 400,

        "error_message": "..."

    }

}




#### DATA
The data key is the meat of the response. It may be a list or dictionary,
but either way this is where you'll find the data you requested.
#### PAGINATION
Sometimes you just can't get enough. For this reason, we've provided a
convenient way to access more data in any request for sequential data.
Simply call the url in the next_url parameter and we'll respond with the
next set of data.

json
{

    ...

    "pagination": {

        "next_url":
"https://api.instagram.com/v1/tags/puppy/media/recent?access_token=fb2e77d.47a0479900504cb3ab4a1f626d174d2d&max_id=13872296",

        "next_max_id": "13872296"

    }

}


On views where pagination is present, we also support the "count" parameter.
Simply set this to the number of items you'd like to receive. Note that the
default values should be fine for most applications - but if you decide to
increase this number there is a maximum value defined on each endpoint.


### JSONP
If you're writing an AJAX application, and you'd like to wrap our response
with a callback, all you have to do is specify a callback parameter with
any API call:


https://api.instagram.com/v1/tags/coffee/media/recent?access_token=fb2e77d.47a0479900504cb3ab4a1f626d174d2d&callback=callbackFunction


Would respond with:

js
callbackFunction({

    ...

});






Contact Information
~~~~~~~~~~~~~~~~~~~


admin



admin@instagram.com



http://instagram.com




License
~~~~~~~


`Instagram License <http://instagram.com>`_




Base URL
~~~~~~~~

http://api.instagram.com/v1


Security
~~~~~~~~


.. _securities_default:

default (HTTP Basic Authentication)
-----------------------------------


*Example with basic auth*




.. _securities_key:

key (API Key)
-------------



**Name:** access_token

**Located in:** query



.. _securities_oauth:

oauth (OAuth 2.0)
-----------------



**Flow:** implicit


**Authorization URL:** https://instagram.com/oauth/authorize/?client_id=CLIENT-ID&redirect_uri=REDIRECT-URI&response_type=token



Scopes
++++++

.. csv-table::
    :header: "Scope", "Description"
    :widths: 10, 50

        basic , "to read any and all data related to a user (e.g. following/followed-by  lists, photos, etc.) (granted by default)"
        comments , "to create or delete comments on a user’s behalf"
        likes , "to like and unlike items on a user’s behalf"
        relationships , "to follow and unfollow users on a user’s behalf"





COMMENTS
~~~~~~~~



DELETE ``/media/{media-id}/comments``
-------------------------------------



Description
+++++++++++

.. raw:: html

    Remove a comment either on the authenticated user's media object or
authored by the authenticated user.


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        media-id | path | Yes | integer |  |  | Media ID


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_2aa04f5eefd0e290e4ee0e5c50cd910a:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | :ref:`data <i_4d863967ef9a9d9efdadd1b250c76bd6>` |  |  |  
        meta | No | :ref:`meta <i_450a11b2a00ff713332f540aadd1c39a>` |  |  |  


**Data schema:**


.. _i_4d863967ef9a9d9efdadd1b250c76bd6:



**Meta schema:**


.. _i_450a11b2a00ff713332f540aadd1c39a:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        code | No | number |  |  |  




**Example:**

.. code-block:: javascript

    {
        "data": {},
        "meta": {
            "code": 5
        }
    }

  


GET ``/media/{media-id}/comments``
----------------------------------



Description
+++++++++++

.. raw:: html

    Get a list of recent comments on a media object.


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        media-id | path | Yes | integer |  |  | Media ID


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_82d909982c7d9bf8ddf3eecf52c96574:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`Comment <d_cca81ed62579b181635d55172acf0075>` |  |  |  
        meta | No | :ref:`meta <i_450a11b2a00ff713332f540aadd1c39a>` |  |  |  




**Meta schema:**


.. _i_450a11b2a00ff713332f540aadd1c39a:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        code | No | number |  |  |  




**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "created_time": "value",
                "from": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "some_login"
                },
                "id": "value",
                "text": "value"
            },
            {
                "created_time": "value",
                "from": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "some_login"
                },
                "id": "value",
                "text": "value"
            },
            {
                "created_time": "value",
                "from": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "some_login"
                },
                "id": "value",
                "text": "value"
            }
        ],
        "meta": {
            "code": 5
        }
    }

  


POST ``/media/{media-id}/comments``
-----------------------------------



Description
+++++++++++

.. raw:: html

    Create a comment on a media object with the following rules:

* The total length of the comment cannot exceed 300 characters.
* The comment cannot contain more than 4 hashtags.
* The comment cannot contain more than 1 URL.
* The comment cannot consist of all capital letters.


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        media-id | path | Yes | integer |  |  | Media ID


Request
+++++++



Body
^^^^


.. _i_fab66249d3aaaacbb736feef8e051a9f:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        TEXT | No | number |  |  |  



.. code-block:: javascript

    5


Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_2aa04f5eefd0e290e4ee0e5c50cd910a:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | :ref:`data <i_4d863967ef9a9d9efdadd1b250c76bd6>` |  |  |  
        meta | No | :ref:`meta <i_450a11b2a00ff713332f540aadd1c39a>` |  |  |  


**Data schema:**


.. _i_4d863967ef9a9d9efdadd1b250c76bd6:



**Meta schema:**


.. _i_450a11b2a00ff713332f540aadd1c39a:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        code | No | number |  |  |  




**Example:**

.. code-block:: javascript

    {
        "data": {},
        "meta": {
            "code": 5
        }
    }

  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`oauth <securities_oauth>`, "comments"


  

DEFAULT
~~~~~~~



GET ``/geographies/{geo-id}/media/recent``
------------------------------------------



Description
+++++++++++

.. raw:: html

    Get recent media from a geography subscription that you created.
**Note**: You can only access Geographies that were explicitly created
by your OAuth client. Check the Geography Subscriptions section of the
[real-time updates page](https://instagram.com/developer/realtime/).
When you create a subscription to some geography
that you define, you will be returned a unique geo-id that can be used
in this query. To backfill photos from the location covered by this
geography, use the [media search endpoint
](https://instagram.com/developer/endpoints/media/).


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        count | query | No | integer |  |  | Max number of media to return.
        min_id | query | No | integer |  |  | Return media before this `min_id`.
        geo-id | path | Yes | integer |  |  | Geolocation ID


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

  

  

LIKES
~~~~~



DELETE ``/media/{media-id}/likes``
----------------------------------



Description
+++++++++++

.. raw:: html

    Remove a like on this media by the currently authenticated user.


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        media-id | path | Yes | integer |  |  | Media ID


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_2aa04f5eefd0e290e4ee0e5c50cd910a:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | :ref:`data <i_4d863967ef9a9d9efdadd1b250c76bd6>` |  |  |  
        meta | No | :ref:`meta <i_450a11b2a00ff713332f540aadd1c39a>` |  |  |  


**Data schema:**


.. _i_4d863967ef9a9d9efdadd1b250c76bd6:



**Meta schema:**


.. _i_450a11b2a00ff713332f540aadd1c39a:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        code | No | number |  |  |  




**Example:**

.. code-block:: javascript

    {
        "data": {},
        "meta": {
            "code": 5
        }
    }

  


GET ``/media/{media-id}/likes``
-------------------------------



Description
+++++++++++

.. raw:: html

    Get a list of users who have liked this media.


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        media-id | path | Yes | integer |  |  | Media ID


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_229123b28fb44e562396f0d89bd1da5e:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`Like <d_15b8732e3f923646eedd5e9758afe36d>` |  |  |  
        meta | No | :ref:`meta <i_450a11b2a00ff713332f540aadd1c39a>` |  |  |  




**Meta schema:**


.. _i_450a11b2a00ff713332f540aadd1c39a:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        code | No | number |  |  |  




**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "first_name": "value",
                "id": "value",
                "last_name": "value",
                "type": "value",
                "user_name": "value"
            },
            {
                "first_name": "value",
                "id": "value",
                "last_name": "value",
                "type": "value",
                "user_name": "value"
            },
            {
                "first_name": "value",
                "id": "value",
                "last_name": "value",
                "type": "value",
                "user_name": "value"
            }
        ],
        "meta": {
            "code": 5
        }
    }

  


POST ``/media/{media-id}/likes``
--------------------------------



Description
+++++++++++

.. raw:: html

    Set a like on this media by the currently authenticated user.

Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        media-id | path | Yes | integer |  |  | Media ID


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_2aa04f5eefd0e290e4ee0e5c50cd910a:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | :ref:`data <i_4d863967ef9a9d9efdadd1b250c76bd6>` |  |  |  
        meta | No | :ref:`meta <i_450a11b2a00ff713332f540aadd1c39a>` |  |  |  


**Data schema:**


.. _i_4d863967ef9a9d9efdadd1b250c76bd6:



**Meta schema:**


.. _i_450a11b2a00ff713332f540aadd1c39a:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        code | No | number |  |  |  




**Example:**

.. code-block:: javascript

    {
        "data": {},
        "meta": {
            "code": 5
        }
    }

  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`oauth <securities_oauth>`, "comments"


  

LOCATION
~~~~~~~~



GET ``/locations/{location-id}``
--------------------------------



Description
+++++++++++

.. raw:: html

    Get information about a location.

Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        location-id | path | Yes | integer |  |  | Location ID


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_97d0e2e68c06f6294b24a57b1baad84a:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | :ref:`Location <d_2fb3f7808cf0d7285b3083152a08f4fb>` |  |  |  




**Example:**

.. code-block:: javascript

    {
        "data": {
            "id": "value",
            "latitude": 5,
            "longitude": 5,
            "name": "value"
        }
    }

  


GET ``/locations/{location-id}/media/recent``
---------------------------------------------



Description
+++++++++++

.. raw:: html

    Get a list of recent media objects from a given location.

Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        max_timestamp | query | No | integer |  |  | Return media before this UNIX timestamp.
        min_timestamp | query | No | integer |  |  | Return media after this UNIX timestamp.
        min_id | query | No | string |  |  | Return media later than this min_id.
        max_id | query | No | string |  |  | Return media earlier than this max_id.
        location-id | path | Yes | integer |  |  | Location ID


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_e1c1e5dc7f4a9acaa4838f0f2d7151ba:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`Media <d_a39c3a3103d212b8befef665ee4528b3>` |  |  |  






**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            },
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            },
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            }
        ]
    }

  


GET ``/locations/search``
-------------------------



Description
+++++++++++

.. raw:: html

    Search for a location by geographic coordinate.

Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        distance | query | No | integer |  |  | Default is 1000m (distance=1000), max distance is 5000.
        facebook_places_id | query | No | integer |  |  | Returns a location mapped off of a Facebook places id. If used, a Foursquare id and lat, lng are not required. 
        foursquare_id | query | No | integer |  |  | returns a location mapped off of a foursquare v1 api location id. If used, you are not required to use lat and lng. Note that this method is deprecated; you should use the new foursquare IDs with V2 of their API. 
        lat | query | No | number |  |  | atitude of the center search coordinate. If used, lng is required. 
        lng | query | No | number |  |  | ongitude of the center search coordinate. If used, lat is required. 
        foursquare_v2_id | query | No | integer |  |  | Returns a location mapped off of a foursquare v2 api location id. If used, you are not required to use lat and lng. 


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_7b2d289da06d38df4399d861935317c4:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`Location <d_2fb3f7808cf0d7285b3083152a08f4fb>` |  |  |  






**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "id": "value",
                "latitude": 5,
                "longitude": 5,
                "name": "value"
            },
            {
                "id": "value",
                "latitude": 5,
                "longitude": 5,
                "name": "value"
            },
            {
                "id": "value",
                "latitude": 5,
                "longitude": 5,
                "name": "value"
            }
        ]
    }

  

  

MEDIA
~~~~~


At this time, uploading via the API is not possible. We made a conscious
choice not to add this for the following reasons:


* Instagram is about your life on the go – we hope to encourage photos

  from within the app.

* We want to fight spam & low quality photos. Once we allow uploading

  from other sources, it's harder to control what comes into the Instagram

  ecosystem. All this being said, we're working on ways to ensure users

  have a consistent and high-quality experience on our platform.





GET ``/locations/{location-id}/media/recent``
---------------------------------------------



Description
+++++++++++

.. raw:: html

    Get a list of recent media objects from a given location.

Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        max_timestamp | query | No | integer |  |  | Return media before this UNIX timestamp.
        min_timestamp | query | No | integer |  |  | Return media after this UNIX timestamp.
        min_id | query | No | string |  |  | Return media later than this min_id.
        max_id | query | No | string |  |  | Return media earlier than this max_id.
        location-id | path | Yes | integer |  |  | Location ID


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_e1c1e5dc7f4a9acaa4838f0f2d7151ba:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`Media <d_a39c3a3103d212b8befef665ee4528b3>` |  |  |  






**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            },
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            },
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            }
        ]
    }

  


GET ``/media1/{shortcode}``
---------------------------



Description
+++++++++++

.. raw:: html

    This endpoint returns the same response as **GET** `/media/media-id`.

A media object's shortcode can be found in its shortlink URL.
An example shortlink is `http://instagram.com/p/D/`
Its corresponding shortcode is D.


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        shortcode | path | Yes | string |  |  | The media shortcode


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
Type: :ref:`Media <d_a39c3a3103d212b8befef665ee4528b3>`


**Example:**

.. code-block:: javascript

    {
        "comments:": {
            "count": 5,
            "data": [
                {
                    "created_time": "value",
                    "from": {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    "id": "value",
                    "text": "value"
                },
                {
                    "created_time": "value",
                    "from": {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    "id": "value",
                    "text": "value"
                },
                {
                    "created_time": "value",
                    "from": {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    "id": "value",
                    "text": "value"
                }
            ]
        },
        "created_time": 5,
        "filter": "value",
        "id": 5,
        "images": {
            "low_resolution": {
                "height": 5,
                "url": "value",
                "width": 5
            },
            "standard_resolution": {
                "height": 5,
                "url": "value",
                "width": 5
            },
            "thumbnail": {
                "height": 5,
                "url": "value",
                "width": 5
            }
        },
        "likes": {
            "count": 10,
            "data": [
                {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "liked_user"
                },
                {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "liked_user"
                },
                {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "liked_user"
                }
            ]
        },
        "location": {
            "id": "value",
            "latitude": 5,
            "longitude": 5,
            "name": "value"
        },
        "tags": [
            {
                "media_count": 5,
                "name": "value"
            },
            {
                "media_count": 5,
                "name": "value"
            },
            {
                "media_count": 5,
                "name": "value"
            }
        ],
        "type": "value",
        "user": {
            "full_name": "John Smith",
            "id": 5,
            "profile_picture": "value",
            "user_name": "my_login"
        },
        "users_in_photo": [
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            },
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            },
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            }
        ],
        "videos": {
            "low_resolution": {
                "height": 5,
                "url": "value",
                "width": 5
            },
            "standard_resolution": {
                "height": 5,
                "url": "value",
                "width": 5
            }
        }
    }

  


GET ``/media/{media-id}``
-------------------------



Description
+++++++++++

.. raw:: html

    Get information about a media object.
The returned type key will allow you to differentiate between `image`
and `video` media.

Note: if you authenticate with an OAuth Token, you will receive the
`user_has_liked` key which quickly tells you whether the current user
has liked this media item.


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        media-id | path | Yes | integer |  |  | The media ID


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
Type: :ref:`Media <d_a39c3a3103d212b8befef665ee4528b3>`


**Example:**

.. code-block:: javascript

    {
        "comments:": {
            "count": 5,
            "data": [
                {
                    "created_time": "value",
                    "from": {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    "id": "value",
                    "text": "value"
                },
                {
                    "created_time": "value",
                    "from": {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    "id": "value",
                    "text": "value"
                },
                {
                    "created_time": "value",
                    "from": {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    "id": "value",
                    "text": "value"
                }
            ]
        },
        "created_time": 5,
        "filter": "value",
        "id": 5,
        "images": {
            "low_resolution": {
                "height": 5,
                "url": "value",
                "width": 5
            },
            "standard_resolution": {
                "height": 5,
                "url": "value",
                "width": 5
            },
            "thumbnail": {
                "height": 5,
                "url": "value",
                "width": 5
            }
        },
        "likes": {
            "count": 10,
            "data": [
                {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "liked_user"
                },
                {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "liked_user"
                },
                {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "liked_user"
                }
            ]
        },
        "location": {
            "id": "value",
            "latitude": 5,
            "longitude": 5,
            "name": "value"
        },
        "tags": [
            {
                "media_count": 5,
                "name": "value"
            },
            {
                "media_count": 5,
                "name": "value"
            },
            {
                "media_count": 5,
                "name": "value"
            }
        ],
        "type": "value",
        "user": {
            "full_name": "John Smith",
            "id": 5,
            "profile_picture": "value",
            "user_name": "my_login"
        },
        "users_in_photo": [
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            },
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            },
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            }
        ],
        "videos": {
            "low_resolution": {
                "height": 5,
                "url": "value",
                "width": 5
            },
            "standard_resolution": {
                "height": 5,
                "url": "value",
                "width": 5
            }
        }
    }

  


GET ``/media/{media-id}/likes``
-------------------------------



Description
+++++++++++

.. raw:: html

    Get a list of users who have liked this media.


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        media-id | path | Yes | integer |  |  | Media ID


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_229123b28fb44e562396f0d89bd1da5e:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`Like <d_15b8732e3f923646eedd5e9758afe36d>` |  |  |  
        meta | No | :ref:`meta <i_450a11b2a00ff713332f540aadd1c39a>` |  |  |  




**Meta schema:**


.. _i_450a11b2a00ff713332f540aadd1c39a:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        code | No | number |  |  |  




**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "first_name": "value",
                "id": "value",
                "last_name": "value",
                "type": "value",
                "user_name": "value"
            },
            {
                "first_name": "value",
                "id": "value",
                "last_name": "value",
                "type": "value",
                "user_name": "value"
            },
            {
                "first_name": "value",
                "id": "value",
                "last_name": "value",
                "type": "value",
                "user_name": "value"
            }
        ],
        "meta": {
            "code": 5
        }
    }

  


GET ``/media/popular``
----------------------



Description
+++++++++++

.. raw:: html

    Get a list of what media is most popular at the moment.
Can return mix of image and video types.



Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_e1c1e5dc7f4a9acaa4838f0f2d7151ba:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`Media <d_a39c3a3103d212b8befef665ee4528b3>` |  |  |  






**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            },
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            },
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            }
        ]
    }

  


GET ``/media/search``
---------------------



Description
+++++++++++

.. raw:: html

    Search for media in a given area. The default time span is set to 5
days. The time span must not exceed 7 days. Defaults time stamps cover
the last 5 days. Can return mix of image and video types.


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        LAT | query | No | number |  |  | Latitude of the center search coordinate. If used, lng is required. 
        MIN_TIMESTAMP | query | No | integer |  |  | A unix timestamp. All media returned will be taken later than this timestamp. 
        LNG | query | No | number |  |  | Longitude of the center search coordinate. If used, lat is required. 
        MAX_TIMESTAMP | query | No | integer |  |  | A unix timestamp. All media returned will be taken earlier than this timestamp. 
        DISTANCE | query | No | integer |  | {"default": 1000, "exclusive_maximum": false, "maximum": 5000} | Default is 1km (distance=1000), max distance is 5km.


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_ccda1a381f1d1c332aaaff7d7fdad7d4:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`Media <d_a39c3a3103d212b8befef665ee4528b3>` extended :ref:`inline <i_7f56d412470cec69d9e195ef5fc21265>` |  |  |  




**Data schema:**


:ref:`Media <d_a39c3a3103d212b8befef665ee4528b3>` extended :ref:`inline <i_7f56d412470cec69d9e195ef5fc21265>`

**Inline schema:**


.. _i_7f56d412470cec69d9e195ef5fc21265:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        comments: | No | :ref:`comments: <i_fbbabd8183306b513d9c1702a1ea41c0>` |  |  |  
        created_time | No | integer |  |  | Epoc time (ms) 
        distance | No | number |  |  |  
        filter | No | string |  |  |  
        id | No | integer |  |  |  
        images | No | :ref:`images <i_0e4bd8ef3ecb86e88cbf9a8cd3a03340>` |  |  |  
        likes | No | :ref:`likes <i_b5fc261f3e95fbb277785b03ecde9c4d>` |  |  |  
        location | No | :ref:`Location <d_2fb3f7808cf0d7285b3083152a08f4fb>` |  |  |  
        tags | No | array of :ref:`Tag <d_3d18743e497cbd847973ac9befcaf218>` |  |  |  
        type | No | string |  |  |  
        user | No | :ref:`MiniProfile <d_8c06519860b7f09c68e31a41b8acb68e>` |  |  |  
        users_in_photo | No | array of :ref:`MiniProfile <d_8c06519860b7f09c68e31a41b8acb68e>` |  |  |  
        videos | No | :ref:`videos <i_83f3c29f6a4a3866a9b917cf8f58fa8b>` |  |  |  




**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "distance": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            },
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "distance": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            },
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "distance": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            }
        ]
    }

  


POST ``/media/{media-id}/comments``
-----------------------------------



Description
+++++++++++

.. raw:: html

    Create a comment on a media object with the following rules:

* The total length of the comment cannot exceed 300 characters.
* The comment cannot contain more than 4 hashtags.
* The comment cannot contain more than 1 URL.
* The comment cannot consist of all capital letters.


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        media-id | path | Yes | integer |  |  | Media ID


Request
+++++++



Body
^^^^


.. _i_fab66249d3aaaacbb736feef8e051a9f:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        TEXT | No | number |  |  |  



.. code-block:: javascript

    5


Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_2aa04f5eefd0e290e4ee0e5c50cd910a:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | :ref:`data <i_4d863967ef9a9d9efdadd1b250c76bd6>` |  |  |  
        meta | No | :ref:`meta <i_450a11b2a00ff713332f540aadd1c39a>` |  |  |  


**Data schema:**


.. _i_4d863967ef9a9d9efdadd1b250c76bd6:



**Meta schema:**


.. _i_450a11b2a00ff713332f540aadd1c39a:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        code | No | number |  |  |  




**Example:**

.. code-block:: javascript

    {
        "data": {},
        "meta": {
            "code": 5
        }
    }

  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`oauth <securities_oauth>`, "comments"


  

RELATIONSHIPS
~~~~~~~~~~~~~


Relationships are expressed using the following terms:

**outgoing_status**: Your relationship to the user. Can be "follows",
  "requested", "none".
**incoming_status**: A user's relationship to you. Can be "followed_by",
  "requested_by", "blocked_by_you", "none".





GET ``/users/self/requested-by``
--------------------------------



Description
+++++++++++

.. raw:: html

    List the users who have requested this user's permission to follow.



Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_5cbc213907f826185e27eff23a27a0e0:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`MiniProfile <d_8c06519860b7f09c68e31a41b8acb68e>` |  |  |  
        meta | No | :ref:`meta <i_c1f2e1c320752464d618edd78a595216>` |  |  |  


**Meta schema:**


.. _i_c1f2e1c320752464d618edd78a595216:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        code | No | integer |  |  |  






**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            },
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            },
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            }
        ],
        "meta": {
            "code": 5
        }
    }

  


GET ``/users/{user-id}/followed-by``
------------------------------------



Description
+++++++++++

.. raw:: html

    Get the list of users this user is followed by.

Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        user-id | path | Yes | number |  |  | The user identifier number


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_7babfbe6d1e7e2238b2a37988688e3c8:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`MiniProfile <d_8c06519860b7f09c68e31a41b8acb68e>` |  |  |  






**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            },
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            },
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            }
        ]
    }

  


GET ``/users/{user-id}/follows``
--------------------------------



Description
+++++++++++

.. raw:: html

    Get the list of users this user follows.

Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        user-id | path | Yes | number |  |  | The user identifier number


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_7babfbe6d1e7e2238b2a37988688e3c8:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`MiniProfile <d_8c06519860b7f09c68e31a41b8acb68e>` |  |  |  






**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            },
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            },
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            }
        ]
    }

  


POST ``/users/{user-id}/relationship``
--------------------------------------



Description
+++++++++++

.. raw:: html

    Modify the relationship between the current user and thetarget user.


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        user-id | path | Yes | number |  |  | The user identifier number


Request
+++++++



Body
^^^^


.. _i_fc6388eae44e0e515e56422c73af661b:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        action | No | string |  | {'enum': ['follow', 'unfollow', 'block', 'unblock', 'approve']} |  



.. code-block:: javascript

    "approve"


Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_7babfbe6d1e7e2238b2a37988688e3c8:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`MiniProfile <d_8c06519860b7f09c68e31a41b8acb68e>` |  |  |  






**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "full_name": "Dave Murray",
                "id": 10,
                "profile_picture": "picture",
                "user_name": "dave"
            },
            {
                "full_name": "Dave Murray",
                "id": 10,
                "profile_picture": "picture",
                "user_name": "dave"
            },
            {
                "full_name": "Dave Murray",
                "id": 10,
                "profile_picture": "picture",
                "user_name": "dave"
            }
        ]
    }

  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`oauth <securities_oauth>`, "relationships"


  

TAGS
~~~~



GET ``/tags/search``
--------------------




Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        q | query | No | string |  |  | A valid tag name without a leading #. (eg. snowy, nofilter) 


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_d55620ae8255c409228e4c6edbf52632:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`Tag <d_3d18743e497cbd847973ac9befcaf218>` |  |  |  
        meta | No | :ref:`meta <i_c1f2e1c320752464d618edd78a595216>` |  |  |  


**Meta schema:**


.. _i_c1f2e1c320752464d618edd78a595216:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        code | No | integer |  |  |  






**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "media_count": 5,
                "name": "value"
            },
            {
                "media_count": 5,
                "name": "value"
            },
            {
                "media_count": 5,
                "name": "value"
            }
        ],
        "meta": {
            "code": 5
        }
    }

  


GET ``/tags/{tag-name}``
------------------------



Description
+++++++++++

.. raw:: html

    Get information about a tag object.

Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        tag-name | path | Yes | string |  |  | Tag name


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
Type: :ref:`Tag <d_3d18743e497cbd847973ac9befcaf218>`


**Example:**

.. code-block:: javascript

    {
        "media_count": 5,
        "name": "value"
    }

  


GET ``/tags/{tag-name}/media/recent``
-------------------------------------



Description
+++++++++++

.. raw:: html

    Get a list of recently tagged media. Use the `max_tag_id` and
`min_tag_id` parameters in the pagination response to paginate through
these objects.


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        tag-name | path | Yes | string |  |  | Tag name


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_3b2f11bdf84d3020293ef09b220dda71:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`Tag <d_3d18743e497cbd847973ac9befcaf218>` |  |  |  






**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "media_count": 5,
                "name": "value"
            },
            {
                "media_count": 5,
                "name": "value"
            },
            {
                "media_count": 5,
                "name": "value"
            }
        ]
    }

  

  

USERS
~~~~~



GET ``/users/search``
---------------------



Description
+++++++++++

.. raw:: html

    Search for a user by name.

Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        q | query | Yes | string |  |  | A query string
        count | query | No | string |  |  | Number of users to return.


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_2cbd80090c7880820a86ed6c035456f5:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`MiniProfile <d_8c06519860b7f09c68e31a41b8acb68e>` |  |  |  






**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            },
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            },
            {
                "full_name": "John Smith",
                "id": 5,
                "profile_picture": "value",
                "user_name": "some_login"
            }
        ]
    }

  


GET ``/users/self/feed``
------------------------



Description
+++++++++++

.. raw:: html

    See the authenticated user's feed.

Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        count | query | No | integer |  |  | Count of media to return.
        max_id | query | No | integer |  |  | Return media earlier than this max_id.s
        min_id | query | No | integer |  |  | Return media later than this min_id.


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_e1c1e5dc7f4a9acaa4838f0f2d7151ba:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`Media <d_a39c3a3103d212b8befef665ee4528b3>` |  |  |  






**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            },
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            },
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            }
        ]
    }

  


GET ``/users/self/media/liked``
-------------------------------



Description
+++++++++++

.. raw:: html

    See the list of media liked by the authenticated user.
Private media is returned as long as the authenticated user
has permissionto view that media. Liked media lists are only
available for the currently authenticated user.


Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        count | query | No | integer |  |  | Count of media to return.
        max_like_id | query | No | integer |  |  | Return media liked before this id.


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

OK

 
**Response Schema:**


.. _i_e1c1e5dc7f4a9acaa4838f0f2d7151ba:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`Media <d_a39c3a3103d212b8befef665ee4528b3>` |  |  |  






**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            },
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            },
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            }
        ]
    }

  


GET ``/users/{user-id}``
------------------------



Description
+++++++++++

.. raw:: html

    Get basic information about a user.

Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        user-id | path | Yes | number |  |  | The user identifier number


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

The user object

 
**Response Schema:**


.. _i_321e87d08779bf67a64c3148b5a40988:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | :ref:`User <d_08e18281892e92ee31598debae39c7be>` |  |  |  




**Example:**

.. code-block:: javascript

    {
        "data": {
            "bio": "value",
            "counts": {
                "follows": 5,
                "follwed_by": 5,
                "media": 5
            },
            "full_name": "value",
            "id": 5,
            "profile_picture": "value",
            "username": "value",
            "website": "value"
        }
    }

  

Security
++++++++

.. csv-table::
    :header: "Security Schema", "Scopes"
    :widths: 15, 45

        :ref:`default <securities_default>`, ""
        :ref:`key <securities_key>`, ""
        :ref:`oauth <securities_oauth>`, "basic"



GET ``/users/{user-id}/media/recent``
-------------------------------------




Parameters
++++++++++

.. csv-table::
    :delim: |
    :header: "Name", "Located in", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 15, 10, 10, 10, 20, 30

        count | query | No | integer |  |  | Count of media to return.
        max_timestamp | query | No | integer |  |  | Return media before this UNIX timestamp.
        min_timestamp | query | No | integer |  |  | Return media after this UNIX timestamp.
        min_id | query | No | string |  |  | Return media later than this min_id.
        max_id | query | No | string |  |  | Return media earlier than this max_id.
        user-id | path | Yes | number |  |  | The user identifier number


Request
+++++++



Responses
+++++++++

**200**
^^^^^^^

Get the most recent media published by a user. To get the most recent
media published by the owner of the access token, you can use `self`
instead of the `user-id`.


 
**Response Schema:**


.. _i_e1c1e5dc7f4a9acaa4838f0f2d7151ba:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        data | No | array of :ref:`Media <d_a39c3a3103d212b8befef665ee4528b3>` |  |  |  






**Example:**

.. code-block:: javascript

    {
        "data": [
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            },
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            },
            {
                "comments:": {
                    "count": 5,
                    "data": [
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        },
                        {
                            "created_time": "value",
                            "from": {
                                "full_name": "John Smith",
                                "id": 5,
                                "profile_picture": "value",
                                "user_name": "some_login"
                            },
                            "id": "value",
                            "text": "value"
                        }
                    ]
                },
                "created_time": 5,
                "filter": "value",
                "id": 5,
                "images": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "thumbnail": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                },
                "likes": {
                    "count": 10,
                    "data": [
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        },
                        {
                            "full_name": "John Smith",
                            "id": 5,
                            "profile_picture": "value",
                            "user_name": "liked_user"
                        }
                    ]
                },
                "location": {
                    "id": "value",
                    "latitude": 5,
                    "longitude": 5,
                    "name": "value"
                },
                "tags": [
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    },
                    {
                        "media_count": 5,
                        "name": "value"
                    }
                ],
                "type": "value",
                "user": {
                    "full_name": "John Smith",
                    "id": 5,
                    "profile_picture": "value",
                    "user_name": "my_login"
                },
                "users_in_photo": [
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    },
                    {
                        "full_name": "John Smith",
                        "id": 5,
                        "profile_picture": "value",
                        "user_name": "some_login"
                    }
                ],
                "videos": {
                    "low_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    },
                    "standard_resolution": {
                        "height": 5,
                        "url": "value",
                        "width": 5
                    }
                }
            }
        ]
    }

  

  
  
Data Structures
~~~~~~~~~~~~~~~


Comment Model Structure
-----------------------


.. _d_cca81ed62579b181635d55172acf0075:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        created_time | No | string |  |  |  
        from | No | :ref:`MiniProfile <d_8c06519860b7f09c68e31a41b8acb68e>` |  |  |  
        id | No | string |  |  |  
        text | No | string |  |  |  


Image Model Structure
---------------------


.. _d_a9a8f383e5aa70107a4b4ba3504468dc:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        height | No | integer |  |  |  
        url | No | string |  |  |  
        width | No | integer |  |  |  


Like Model Structure
--------------------


.. _d_15b8732e3f923646eedd5e9758afe36d:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        first_name | No | string |  |  |  
        id | No | string |  |  |  
        last_name | No | string |  |  |  
        type | No | string |  |  |  
        user_name | No | string |  |  |  


Location Model Structure
------------------------


.. _d_2fb3f7808cf0d7285b3083152a08f4fb:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        id | No | string |  |  |  
        latitude | No | number |  |  |  
        longitude | No | number |  |  |  
        name | No | string |  |  |  


Media Model Structure
---------------------


.. _d_a39c3a3103d212b8befef665ee4528b3:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        comments: | No | :ref:`comments: <i_fbbabd8183306b513d9c1702a1ea41c0>` |  |  |  
        created_time | No | integer |  |  | Epoc time (ms) 
        filter | No | string |  |  |  
        id | No | integer |  |  |  
        images | No | :ref:`images <i_0e4bd8ef3ecb86e88cbf9a8cd3a03340>` |  |  |  
        likes | No | :ref:`likes <i_b5fc261f3e95fbb277785b03ecde9c4d>` |  |  |  
        location | No | :ref:`Location <d_2fb3f7808cf0d7285b3083152a08f4fb>` |  |  |  
        tags | No | array of :ref:`Tag <d_3d18743e497cbd847973ac9befcaf218>` |  |  |  
        type | No | string |  |  |  
        user | No | :ref:`MiniProfile <d_8c06519860b7f09c68e31a41b8acb68e>` |  |  |  
        users_in_photo | No | array of :ref:`MiniProfile <d_8c06519860b7f09c68e31a41b8acb68e>` |  |  |  
        videos | No | :ref:`videos <i_83f3c29f6a4a3866a9b917cf8f58fa8b>` |  |  |  


**Comments: schema:**


.. _i_fbbabd8183306b513d9c1702a1ea41c0:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        count | No | integer |  |  |  
        data | No | array of :ref:`Comment <d_cca81ed62579b181635d55172acf0075>` |  |  |  




**Images schema:**


.. _i_0e4bd8ef3ecb86e88cbf9a8cd3a03340:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        low_resolution | No | :ref:`Image <d_a9a8f383e5aa70107a4b4ba3504468dc>` |  |  |  
        standard_resolution | No | :ref:`Image <d_a9a8f383e5aa70107a4b4ba3504468dc>` |  |  |  
        thumbnail | No | :ref:`Image <d_a9a8f383e5aa70107a4b4ba3504468dc>` |  |  |  


**Likes schema:**


.. _i_b5fc261f3e95fbb277785b03ecde9c4d:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        count | No | integer |  |  |  
        data | No | array of :ref:`MiniProfile <d_8c06519860b7f09c68e31a41b8acb68e>` |  |  |  








**Videos schema:**


.. _i_83f3c29f6a4a3866a9b917cf8f58fa8b:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        low_resolution | No | :ref:`Image <d_a9a8f383e5aa70107a4b4ba3504468dc>` |  |  |  
        standard_resolution | No | :ref:`Image <d_a9a8f383e5aa70107a4b4ba3504468dc>` |  |  |  


MiniProfile Model Structure
---------------------------


.. _d_8c06519860b7f09c68e31a41b8acb68e:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        full_name | No | string |  |  |  
        id | No | integer |  |  |  
        profile_picture | No | string |  |  |  
        user_name | No | string |  |  |  


Tag Model Structure
-------------------


.. _d_3d18743e497cbd847973ac9befcaf218:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        media_count | No | integer |  |  |  
        name | No | string |  |  |  


User Model Structure
--------------------


.. _d_08e18281892e92ee31598debae39c7be:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        bio | No | string |  |  |  
        counts | No | :ref:`counts <i_3ae25d134242ce362381d3f51962e9be>` |  |  |  
        full_name | No | string |  |  |  
        id | No | integer |  |  |  
        profile_picture | No | string |  |  |  
        username | No | string |  |  |  
        website | No | string |  |  |  


**Counts schema:**


.. _i_3ae25d134242ce362381d3f51962e9be:

.. csv-table::
    :delim: |
    :header: "Name", "Required", "Type", "Format", "Properties", "Description"
    :widths: 20, 10, 15, 15, 30, 25

        follows | No | integer |  |  |  
        follwed_by | No | integer |  |  |  
        media | No | integer |  |  |  


