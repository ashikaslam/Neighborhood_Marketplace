
from.models import User
from.import models
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Products
        exclude = ['user', 'date_of_post','sell_availavle']


class POst_updat_Serializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=15)
    title = serializers.CharField(max_length=15)
    product_picture = serializers.ImageField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description =serializers.CharField()
    category = serializers.CharField()
    condition = serializers.CharField()
    email =serializers.CharField(required=False)





    
    
    
    
    