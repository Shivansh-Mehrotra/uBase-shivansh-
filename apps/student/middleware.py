from .models import RequestResponseLogData
import logging
import traceback
import time

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
#
# class RequestResponseLoggingMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         request.request_body = request.body.decode('utf-8') if request.body else ''
#         request.method_name = request.method
#         request.path_info = request.path_info
#
#     def process_response(self, request, response):
#         if hasattr(request, 'method_name'):
#            # print('im here')
#             RequestResponseLogData.objects.create(
#                 path=request.path_info,
#                 method=request.method_name,
#                 request_body=request.request_body,
#                 response_body=response.content.decode('utf-8'),
#                 status_code=response.status_code
#             )
#         return response



class RequestResponseLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        request_body = request.body
        try:

            response = self.get_response(request)
            if response.status_code!=200:
                print(response)
                self.log_failed_request(request, response, request_body)
            else:
                duration = time.time() - start_time
                self.log_request_response(request, response ,request_body)

            return response

        except Exception as e:
            duration = time.time() - start_time
            self.log_failed_request(request, e, request_body)

            raise

    def log_request_response(self, request, response,request_body):

        RequestResponseLogData.objects.create(
            path=request.path,
            method=request.method,
            request_body=request_body,
            response_body=response.content.decode('utf-8'),
            status_code=response.status_code
        )

    def log_failed_request(self, request, exception, request_body):

        print(exception)
        error_details = traceback.format_exc()

        RequestResponseLogData.objects.create(
            path=request.path,
            method=request.method,
            request_body=request_body,
            response_body=str(exception),
            error_details=error_details,
            status_code=exception.status_code
        )
