from django.db import models
from rest_framework import serializers
from .models import Userpdfdata

class UserpdfdataSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Userpdfdata
        fields = '__all__'