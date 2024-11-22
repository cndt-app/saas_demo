from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

from demo_app import conduit_api


class ErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, conduit_api.ConduitAPIError):
            return render(request,'views/error.html',{'error': exception})
