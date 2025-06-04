from django.shortcuts import render

# recipes_api/views.py

import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import RecipeRequestSerializer

# Hard-coded Groq key (not recommended in production):
GROQ_API_KEY = "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"

@api_view(["POST"])
@permission_classes([AllowAny])
def generate_recipes(request):
    serializer = RecipeRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    validated = serializer.validated_data
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}"
        }
        payload = {
            "model": validated["model"],
            "messages": [
                { "role": "user", "content": validated["prompt"] }
            ],
            "max_tokens": validated["max_tokens"],
            "temperature": validated["temperature"],
            "top_p": validated["top_p"]
        }

        url = "https://api.groq.com/openai/v1/chat/completions"
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()
        ai_text = data["choices"][0]["message"]["content"]
        return Response({"choices": [{"text": ai_text}]}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
