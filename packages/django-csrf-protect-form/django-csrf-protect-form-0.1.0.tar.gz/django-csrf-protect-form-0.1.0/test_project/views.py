from pprint import pformat

from django.http import HttpResponse


def endpoint(request):
    return HttpResponse('\n'.join([repr(request), pformat(vars(request)), request.body.decode()]), content_type='text/plain')
