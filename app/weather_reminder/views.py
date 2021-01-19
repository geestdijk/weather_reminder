from django.http import JsonResponse
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


def ping(request):
    data = {"ping": "pong!"}
    return JsonResponse(data)


class HelloApiView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        return Response({"greetings": "hello!"})


class HelloTemplateView(TemplateView):
    template_name = "hello.html"
