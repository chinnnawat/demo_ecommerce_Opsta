from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import json

class CheckUserMiddleware(MiddlewareMixin):
    
    def __init__(self, get_response):
        self.get_response = get_response

    # def __call__(self, request):
    #     # Pre-process request
    #     self.process_request(request)
        
    #     # Custom method call
    #     self.custom_method()

    #     # Call the next middleware or view
    #     response = self.get_response(request)

    #     # Post-process response
    #     self.process_response(request, response)

    #     return response

    def process_request(self, request):
        print("Processing request in process_request method")
        # Add custom request processing logic here

    def process_response(self, request, response):
        print("Processing response in process_response method")
        # Add custom response processing logic here
        return response

    def custom_method(self):
        print("Custom method called")
        # Add custom logic here