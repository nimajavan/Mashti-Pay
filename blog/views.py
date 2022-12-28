from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Comment
from .serializer import CommentSerializer
from rest_framework import status


class ApiTest(APIView):

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
