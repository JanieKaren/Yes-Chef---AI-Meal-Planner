# recipes_api/serializers.py
from rest_framework import serializers

class RecipeRequestSerializer(serializers.Serializer):
    model = serializers.CharField(default="meta-llama/llama-4-scout-17b-16e-instruct")
    prompt = serializers.CharField()
    max_tokens = serializers.IntegerField(default=500)
    temperature = serializers.FloatField(default=0.7)
    top_p = serializers.FloatField(default=0.9)
