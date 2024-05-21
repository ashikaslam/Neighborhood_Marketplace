from django.shortcuts import render

# Create your views here.



from django.shortcuts import render,redirect





# models 
from user_accounts_manager.models import User
from.import models


# serializers 
from. import  serializers 

# rest_fremwork 
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework import status

# python 
import random

# django 

from django.contrib.auth import authenticate, login,logout
from django.http import JsonResponse
from django.utils.http import urlencode
# email send moudles
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



# main code .......................


class create_sell_post(APIView):
    authentication_classes=[JWTAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProductsSerializer
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                    the_product = serializer.save()
                    try:
                         the_product.user=request.user
                         the_product.save()
                    except Exception as e: return Response("somethigh went wrong",status=status.HTTP_406_NOT_ACCEPTABLE)
                    psots_picture = request.FILES.get('profile_picture')
                    if psots_picture:
                         try:
                              the_product.product_picture=psots_picture
                              the_product.save()
                         except Exception as e:pass
                    return Response({"status":1})
            except Exception as e:
                 return Response("somethigh went wrong",status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors)







class RecentPost(APIView):
     def get(self, request):
          id_value = request.GET.get('id')
          print("the id is  >>>>", id_value)
          if id_value:
              id_value=int(id_value)
              
              post = models.Products.objects.filter(id=id_value).exists()
              if post:
                   post = models.Products.objects.filter(id=id_value).values()
                   return JsonResponse({'post': list(post)})
              else :return JsonResponse({'error': "post not found"})

          all_post = models.Products.objects.filter().values()
          return JsonResponse({'all_post': list(all_post)})
     


class my_post(APIView):
    authentication_classes=[JWTAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        all_post =user.my_products.all().values()
        return JsonResponse({'all_post': list(all_post)})
    


class delete_my_post(APIView):
    authentication_classes=[JWTAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
          try:
               id_value = request.GET.get('id')
               print("the id is  >>>>", id_value)
               if id_value:
                    id_value=int(id_value)
                    if models.Products.objects.filter(id=id).exists():
                         post = models.Products.objects.get(id=id)
                         if post.user == request.user:
                              post.delete()
                              return Response(status=status.HTTP_200_OK)
          except Exception as e:return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
          return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
                        
                   
        

          
class update_sell_post(APIView):
    authentication_classes=[JWTAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProductsSerializer
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
          try:
               id_value = request.GET.get('id')
               print("the id is  >>>>", id_value)
               if id_value:
                    id_value=int(id_value)
                    if models.Products.objects.filter(id=id_value).exists():
                         post = models.Products.objects.get(id=id_value)
                         if post.user == request.user:
                              serializer = self.serializer_class(data=request.data)
                              if serializer.is_valid():
                                   product_picture = request.FILES.get('product_picture')
                                   if  product_picture:
                                        post.product_picture= product_picture
                                        post.save()
                                   email  = serializer.validated_data['email']
                                   if  product_picture:
                                        post.email= email
                                        post.save()
                                   price  = serializer.validated_data['price']
                                   title  = serializer.validated_data['title']
                                   mobile_number  = serializer.validated_data['mobile_number']
                                   description  = serializer.validated_data['description']
                                   category  = serializer.validated_data['category']
                                   condition  = serializer.validated_data['condition']
                                   post.price=price
                                   post.title=title
                                   post.mobile_number=mobile_number
                                   post.description=description
                                   post.category=category
                                   post.condition=condition
                                   post.save()
                                   return Response('done')
                              return Response(serializer.errors)
                    
          except Exception as e:return Response("somethigh went wrong",status=status.HTTP_406_NOT_ACCEPTABLE)
          return Response("somethigh went wrong",status=status.HTTP_406_NOT_ACCEPTABLE)
  
        

