from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response



class HelloView(APIView):
    def get(self,request):
        return Response({
            'name': 'evan', 'age': 23
        })

    