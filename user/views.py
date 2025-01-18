from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from user import serializers
from book.serializers import BookListSerializer
from book.models import Book


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny, )


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )

    def get_object(self):
        return self.request.user


class MyLibraryView(generics.ListAPIView):
    serializer_class = BookListSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )

    def get_queryset(self):
        queryset = Book.objects.filter(
            users=self.request.user.id
        ).prefetch_related("genres", "authors")

        return queryset
