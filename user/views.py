from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from user import serializers


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        """Registers a new user with email and password"""
        return super().post(request, *args, **kwargs)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        """Returns a detail information about authenticated user"""
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Updated a detail information about authenticated user
        (all the fields should be filled)
        """
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Updated a detail information about authenticated user
        (not all the fields should be filled)
        """
        return super().patch(request, *args, **kwargs)
