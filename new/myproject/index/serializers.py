from django.db import models
from rest_framework import serializers
from .models import stocks_model

class stockserializer(serializers.ModelSerializer):
    class Meta:
        model = stocks_model
        fields = '__all__'