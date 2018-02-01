from rest_framework import serializers
from snippets.models import FaceData, LANGUAGE_CHOICES, STYLE_CHOICES

class FaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceData
        fields = ('identity', 'rep', 'images', 'phash')