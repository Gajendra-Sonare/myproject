from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.http import request
import requests
from rest_framework import response
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import stocks_model
from .serializers import stockserializer
import json
from .stock_prediction import stock_prediction
from django.http import HttpRequest
from .news_sentiment import news_sentiment_analysis


# Create your views here.

class stocks(APIView):

    def post(self,request):

        recieved_data = request.data

        if recieved_data["feature"] =="sentiment analysis":
            df = news_sentiment_analysis(recieved_data["name"])
            return Response(df)

        else:
            df = stock_prediction(recieved_data["name"])
            return Response(df)