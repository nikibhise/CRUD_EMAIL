from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
import logging
from crud_email_pro.utils import send_email
#from django.core.mail import send_mail
#from django.conf import settings

error_logger = logging.getLogger('error_logger')
success_logger = logging.getLogger('success_logger')

class UserAPI(APIView):

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            subject = "Account Creation Successful"
            body = "Hello %s,\n\tThank you for creating account with us " %(serializer.data.get('username'),)
            recipient_list = [serializer.data.get("email"),]
            #send_mail(subject=subject, message=body, from_email=settings.EMAIL_HOST_USER, recipient_list=recipient_list)
            send_email(subject=subject, body=body, recipient_list=recipient_list)
            success_logger.info(f"The user with username: {serializer.data.get('username')} created successfully")
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            error_logger.error(f"Error saving th user data {serializer.errors}")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)