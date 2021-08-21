from django.db.models import fields
from rest_framework import serializers
from .models import *


class information_serializer(serializers.ModelSerializer):
    class Meta:
        model  = information
        fields = "__all__"
