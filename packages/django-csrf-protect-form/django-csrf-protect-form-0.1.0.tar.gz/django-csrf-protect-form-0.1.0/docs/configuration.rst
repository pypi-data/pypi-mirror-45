Configuration
=============

You can set a list of content types which have CSRF protection enabled. The
default value is:

.. code:: python

  CSRF_PROTECT_FORM_CONTENT_TYPE = [
    'application/x-www-form-urlencoded',
    'multipart/form-data',
    'text/plain',
  ]
