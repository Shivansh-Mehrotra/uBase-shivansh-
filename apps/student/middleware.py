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
