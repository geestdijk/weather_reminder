from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Setup
from .serializers import SetupSerializer


class SetupApiView(generics.CreateAPIView):
    serializer_class = SetupSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def delete(self, request, hour, format=None):
        """Deletes a current user's forecast by city name"""
        user = self.request.user

        try:
            setup = Setup.objects.get(user=user, scheduled_time=hour)
        except Setup.DoesNotExist:
            raise Http404("No Setup matches the given query.")
        print("=============")
        setup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionExistsApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, format=None):
        user = self.request.user
        setup_exists = Setup.objects.filter(user=user).last()
        data = {'exists': setup_exists is not None}
        if setup_exists:
            data['time'] = setup_exists.scheduled_time
        return Response(data)
