from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from user.serializers import UserSerializer, User


class Signup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(user_name=request.data['user_name'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        user = get_object_or_404(User, user_name=request.data['user_name'])

        if not user.check_password(request.data['password']):
            return Response("Invalid credentials", status=status.HTTP_404_NOT_FOUND)

        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)

        return Response({'token': token.key, 'user': serializer.data})


class TestToken(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response("passed!")
