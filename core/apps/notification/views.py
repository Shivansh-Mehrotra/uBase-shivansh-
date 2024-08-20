from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status as http_status_codes
from .notification_helper import send_email_notification
import json


class Notification(ViewSet):

    def email_notification(self, request):
        if request.method == 'POST':
            context = request.data
            if context:
                response = send_email_notification(context)
                if response['is_error']:
                    return Response({'message': response['error']}, http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({'message': 'Email Notification Successfully Sent from our end'},
                                    http_status_codes.HTTP_200_OK)
            else:
                return Response({'message': 'mailing information not sent in request'}, http_status_codes.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Get method not allowed'}, http_status_codes.HTTP_405_METHOD_NOT_ALLOWED)

    def sms_notification(self, request):
        pass


