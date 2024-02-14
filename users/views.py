from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView    
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from . import serializers
from .models import User

class Users(APIView):
        
        def post(self, request):
            password = request.data.get("password")
            if not password:
                raise ParseError(detail="Password is required")
            serializer = serializers.PrivateUserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(password)
                user.save()
                serializer = serializers.PrivateUserSerializer(user)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
            
            
class Me(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(data=serializer.data)
    
    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user, 
            data=request.data,
            partial=True,
            )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class PublicUser(APIView):
    
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
class ChangePassword(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password: 
            raise ParseError(detail="old_password and new_password are required")
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status = status.HTTP_200_OK)
        else:
            raise ParseError(detail="old_password is wrong")
        
        
class Login(APIView):
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError(detail="username and password are required")
        user = authenticate(
            request, 
            username=username, 
            password=password
            )
        if user:
            login(request, user)
            return Response({"ok": "success"})
        else:
            return Response({"error": "wrong password"})
        
        
class Logout(APIView):
    
    def post(self, request):
        logout(request)
        return Response({"ok": "bye"})
    


