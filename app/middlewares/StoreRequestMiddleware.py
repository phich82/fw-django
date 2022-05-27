from app.services.Core import Core

class StoreRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Store copy of request for using anywhere
        # Http in python is stateless. Session exists only on each request.
        # so, for using session anywhere, we need to store session first.
        Core.request = request

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
