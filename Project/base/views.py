from rest_framework import status, filters
from rest_framework.generics import *
from .serializers import *
from rest_framework.response import Response
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from itertools import chain
from rest_framework.views import APIView


class RegistrationView(CreateAPIView):
    
    serializer_class = RegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response({"message": "Successful Registration"}, status = status.HTTP_201_CREATED)
    
class WorkView(ListAPIView):
    
    serializer_class = WorkSerializer
    
    def get_queryset(self):
        
        artist_name = self.request.GET.get('artist')
        if artist_name is not None:
            artist = get_object_or_404(Artist, name = artist_name)
            return artist.works
        
        work_type = self.request.GET.get('work_type')
        if work_type is not None:
            return Work.objects.filter(type = work_type)
        
        return Work.objects.all()

