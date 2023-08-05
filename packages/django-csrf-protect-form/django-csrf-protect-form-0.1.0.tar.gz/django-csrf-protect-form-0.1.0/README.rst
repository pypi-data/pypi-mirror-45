.. image:: https://img.shields.io/pypi/v/django-csrf-protect-form.svg
   :target: https://pypi.python.org/pypi/django-csrf-protect-form
.. image:: https://travis-ci.org/dex4er/django-csrf-protect-form.svg?branch=master
   :target: https://travis-ci.org/dex4er/django-csrf-protect-form
.. image:: https://readthedocs.org/projects/django-csrf-protect-form/badge/?version=latest
   :target: http://django-csrf-protect-form.readthedocs.org/en/latest/
.. image:: https://img.shields.io/pypi/pyversions/django-csrf-protect-form.svg
   :target: https://www.python.org/
.. image:: https://img.shields.io/pypi/djversions/django-csrf-protect-form.svg
   :target: https://www.djangoproject.com/

django-csrf-protect-form
========================

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


Installation
------------

Install with ``pip`` or ``pipenv``:

.. code:: python

  pip install django-csrf-protect-form


Configuration
-------------

You can set a list of content types which have CSRF protection enabled. The
default value is:

.. code:: python

  CSRF_PROTECT_FORM_CONTENT_TYPE = [
    'application/x-www-form-urlencoded',
    'multipart/form-data',
    'text/plain',
  ]


Usage
-----

**views.py**

.. code:: python

  from django_csrf_protect_form import csrf_protect_form

  @csrf_protect_form
  def hello(request):
      return HttpResponse("<html><head></head><body>Hello, world!</body></html>")

or:

**urls.py**

.. code:: python

  from django_csrf_protect_form import csrf_protect_form
  from .views import hello

  urlpatterns = [
      url('hello/', csrf_protect_form(hello)),
  ]


Documentation
-------------

See http://django-csrf-protect-form.readthedocs.org/


License
-------

Copyright © 2019, Piotr Roszatycki

This software is distributed under the GNU Lesser General Public License (LGPL
3 or greater).
