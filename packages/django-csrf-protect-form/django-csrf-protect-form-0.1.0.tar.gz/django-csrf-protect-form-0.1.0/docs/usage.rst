Usage
=====

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
