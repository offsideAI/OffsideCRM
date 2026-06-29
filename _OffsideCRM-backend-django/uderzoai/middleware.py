# middleware.py

class DebugCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Log incoming request's origin
        origin = request.META.get('HTTP_ORIGIN')
        print(f"DebugCorsMiddleWare - Request origin: {origin}")
        # Log response headers
        for key, value in response.items():
            print(f"DebugCorsMiddleWare - {key}: {value}")
        return response