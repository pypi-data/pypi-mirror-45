================================================
django-csrf-protect-form |release| documentation
================================================

The CSRF middleware and template tag from Django framework provides easy-to-use
protection against Cross Site Request Forgeries. This protector has some
inconveniences for XHR POST requests.

This module enables CSRF protection only for HTML forms when content type of
the request is one of the following:

* application/x-www-form-urlencoded
* multipart/form-data
* text/plain

It is generally safe to exclude XHR requests from CSRF protection, because XHR
requests can only be made from the same origin. Check your CORS configuration
before using this module. Use `django-cors-headers
<https://github.com/ottoyiu/django-cors-headers>`_ module to protect your site
with CORS.

.. toctree::
    :maxdepth: 2

    installation
    configuration
    usage
    license
