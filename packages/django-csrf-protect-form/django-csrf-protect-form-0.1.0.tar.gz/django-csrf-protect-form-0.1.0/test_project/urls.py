from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django_csrf_protect_form import csrf_protect_form

from .views import endpoint


urlpatterns = [
    url('csrf_default/', endpoint),
    url('csrf_protect/', csrf_protect(endpoint)),
    url('csrf_protect_form/', csrf_protect_form(endpoint)),
    url('csrf_exempt/', csrf_exempt(endpoint)),
]
