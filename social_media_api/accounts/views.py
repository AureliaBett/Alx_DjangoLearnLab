from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, generics
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, UserListSerializer
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import TokenAuthentication
from .models import User as CustomUser

User = get_user_model()

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
class RegisterListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)
    


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "message": "Login successful",
            "token": token.key,
            "username": user.username
        })
class ProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = CustomUser.objects.all()  # <-- satisfies the check
    lookup_url_kwarg = 'user_id'

    def post(self, request, *args, **kwargs):
        target_user = self.get_object()  # uses queryset above
        if target_user == request.user:
            return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.add(target_user)
        return Response({"message": f"You are now following {target_user.username}"}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = CustomUser.objects.all()
    lookup_url_kwarg = 'user_id'

    def post(self, request, *args, **kwargs):
        target_user = self.get_object()
        if target_user == request.user:
            return Response({"error": "You cannot unfollow yourself"}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.remove(target_user)
        return Response({"message": f"You have unfollowed {target_user.username}"}, status=status.HTTP_200_OK)