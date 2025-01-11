from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from book import models, serializers


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
