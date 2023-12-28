import logging
from .models import Library
from .serializers import LibrarySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from crud_email_pro.utils import send_email

error_logger = logging.getLogger('error_logger')
success_logger = logging.getLogger('success_logger')

class CrudAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            books = Library.objects.all()
            serializer = LibrarySerializer(books, many=True)
            success_logger.info("Books fetched successfully")
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error("There is an error")
            return Response(data={'deatil': "There is an error fetching the posts"}, status=status.HTTP_400_BAD_REQUEST)
        

    def post(self, request):
        try:
            serializer = LibrarySerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            body = "Hello %s, You have just created a post %s " %(request.user.username, serializer.data.get('title'))
            subject = "Post created successfully"
            recipient_list = [request.user.email,]
            send_email(subject=subject, body=body, recipient_list=recipient_list)
            success_logger.info(f"Book with id {serializer.data.get('id')} created successfully")
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_logger.error(f"Failed to create book : {serializer.errors}")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
class CrudDetailsAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            books = get_object_or_404(Library, pk=pk)
            serializer = LibrarySerializer(books)
            success_logger.info(f"Books deails fetched : {serializer.data}")
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error(f"There is an error fetching the books")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pk=None):
        try:
            books = get_object_or_404(Library, pk=pk)
            serializer = LibrarySerializer(books, data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                body = "Hello %s, You have just updated a post %s " %(request.user.username, serializer.data.get('title'))
                subject = "Post Updated successfully"
                recipient_list = [request.user.email,]
                send_email(subject=subject, body=body, recipient_list=recipient_list)
                success_logger.info(f"Books updated: {instance}")
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error(f"Failed to update book {pk}: {serializer.errors}")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try: 
            books = get_object_or_404(Library, pk=pk)
            books.save()
            body = "Hello %s, You have just delete a post %s " %(request.user.username,)
            subject = "Post deleted successfully"
            recipient_list = [request.user.email,]
            send_email(subject=subject, body=body, recipient_list=recipient_list)
            success_logger.info(f"Books deleted successfully: {pk}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_logger.error(f"Failed to delete book")
            return Response(data= {'detail': 'Error deleting books'}, status=status.HTTP_400_BAD_REQUEST)  
              


