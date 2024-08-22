from django.utils.deprecation import MiddlewareMixin
from .models import RequestResponseLogData
import logging
logger = logging.getLogger(__name__)

class StudentAppMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"Request method: {request.method}, path: {request.path}")
        if request.method == 'POST' and request.path.startswith('/api/students'):
            logger.info("Processing POST request for /api/students")
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

    def process_exception(self, request, exception):
        return None

    def process_template_response(self, request, response):
        return response

class RequestResponseLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.request_body = request.body.decode('utf-8') if request.body else ''
        request.method_name = request.method
        request.path_info = request.path_info

    def process_response(self, request, response):
        if hasattr(request, 'method_name'):
            RequestResponseLogData.objects.create(
                path=request.path_info,
                method=request.method_name,
                request_body=request.request_body,
                response_body=response.content.decode('utf-8'),
                status_code=response.status_code
            )
        return response
