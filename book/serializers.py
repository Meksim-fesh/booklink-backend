from rest_framework import serializers

from book import models


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Genre
        fields = ["id", "name"]
