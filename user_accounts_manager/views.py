from django.shortcuts import render,redirect





# models 
from.models import User
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
def generate_otp():
        """Generate a random 4-digit OTP."""
        return random.randint(100000, 999999)


class RegistrationVies(APIView):
    serializer_class = serializers.UserRegistrationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                    phone_number = serializer.validated_data['mobile_number']
                    email = serializer.validated_data['email']
                    user = User.objects.filter(mobile_number=phone_number).exists()
                    if user :return Response("we have a a user with this phone number")
                    user = User.objects.filter( email= email).exists()
                    if user :return Response("we have a a user with this  email")
                    user = serializer.save()
                    # Generate OTP
                    otp = generate_otp()
                    user.otp = otp
                    user.save()
                    return Response({"status":1})
            except Exception as e:
                 return Response("somethigh went wrong",status=status.HTTP_406_NOT_ACCEPTABLE)
                 
        return Response(serializer.errors)
    





class Login_api_view(APIView):
    serializer_class = serializers.loginSerializer
    def post(self,request):
        serializer  = self.serializer_class(data=request.data)
        if  serializer.is_valid():
            user_name = serializer .validated_data['user_name']
            password= serializer .validated_data['password']
            phone_number = user_name

            if '@' in user_name or '.com' in user_name:
                user= User.objects.filter(email=user_name).exists()
                if not user or user == None:return Response({'error' : "Invalid Credential"})
                user= User.objects.get(email=user_name)
                phone_number=user.mobile_number
         
            user= User.objects.filter(mobile_number=phone_number).exists()

            if not user or user == None:return Response({'error' : "Invalid Credential"})
            user= User.objects.get(mobile_number=phone_number)
           
            user = authenticate(username=phone_number, password=password)
            
            if not user or user == None:return Response({'error' : "Invalid Credential"})
            # here we got the athenticate user 
            Refresh=RefreshToken.for_user(user)
            login(request,user)
            return Response({ "email":user.email,"access" :str( Refresh.access_token), 'refresh':str( Refresh),'user_id' : user.id,"status":1 ,'user_name':user.name,'mobile_number':user.mobile_number},status=status.HTTP_200_OK)
        
        return Response(serializer.errors)
    




class Logout(APIView):
    authentication_classes=[JWTAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.logoutSerializer
    def post(self, request):
        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid():
            refresh_token  = serializer.validated_data['refresh_token']
            try:
                logout(request)
                RefreshToken(refresh_token).blacklist()
                return Response("successsfully loged out",status=status.HTTP_200_OK)
            except Exception as e:
                    return Response("somethigh went wrong",status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)
    

class apiLogout(APIView):
    serializer_class = serializers.logoutSerializer
    def post(self, request):
        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid():
            refresh_token  = serializer.validated_data['refresh_token']
            try:
                RefreshToken(refresh_token).blacklist()
                return Response("successsfully loged out",status=status.HTTP_200_OK)
            except Exception as e:
                    return Response("somethigh went wrong",status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)

# password set views





class change_pass(APIView):
    authentication_classes=[JWTAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.change_pass
    def post(self, request):
        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid():
            current_passowrd  = serializer.validated_data['current_passowrd']
            try:
                user = authenticate(username=request.user.mobile_number, password=current_passowrd)
                print(user)
                if user==request.user:
                    print(user,request.user)
                    return serializer.save(request.user)
                else :return Response({'error' : "Invalid Credential 99"},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                     return Response({'error' : "Invalid Credential 100"},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)





# user email varify

def send_top(user):
    try:
        otp =generate_otp()
        user.otp = otp
        user.save()
        email_id = user.email
        email_subject = "activaton otp!!!"
        email_body = render_to_string('active_email.html', {'otp' : otp})
        email = EmailMultiAlternatives(email_subject , '', to=[email_id])
        email.attach_alternative(email_body, "text/html")
        email.send()
        return Response({"message":"successsfully email sent","status":1},status=status.HTTP_200_OK)

    except Exception as  e:
               print('here')
               return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

### eamil varfy vies 
class email_varify(APIView):
     authentication_classes=[JWTAuthentication,SessionAuthentication]
     permission_classes = [IsAuthenticated]
     def get(self,request):
          try:
               return  send_top(request.user)
          except Exception as  e:
               return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class Confirm_otp(APIView):
    authentication_classes=[JWTAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.TakeOtpSerializer
    def post(self,request):
        serializer  = self.serializer_class(data=request.data)
        if  serializer.is_valid():
            user = request.user
            otp1 =  serializer .validated_data['otp']
            otp2 =user.otp
            if(otp1!=otp2): return Response({'error' : "Invalid phone number"},status.HTTP_400_BAD_REQUEST)
            if(otp1==otp2):
                 try:
                  user.email_is_varifaied=True
                  user.save()
                  return Response("successsfully confirmed email",status=status.HTTP_200_OK)
                 except Exception as e:
                      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'error' : "Invalid otp"},status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)
    
### eamil varfy viwes   end ..............X.................


# forget pass start...........................
class reset_pass_pre(APIView):
    serializer_class = serializers.Phone_for_forget_pass_Serializer
    def post(self,request):
        serializer  = self.serializer_class(data=request.data)
        if  serializer.is_valid():
            phone  = serializer.validated_data['phone']
            user = User.objects.filter(mobile_number=phone).exists()
            if user:
               try:
                   user = User.objects.get(mobile_number=phone)
                   return send_top(user)
               except Exception as e:
                      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                 return Response({'error' : "Invalid phone number"},status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)
    



class Confirm_otp_pass_change(APIView):
    serializer_class = serializers.TakeOtpSerializer_2
    def post(self,request):
        serializer  = self.serializer_class(data=request.data)
        if  serializer.is_valid():
            phone  = serializer.validated_data['phone']
            user = User.objects.filter(mobile_number=phone).exists()
            if user:
               try:
                   user = User.objects.get(mobile_number=phone)
                   otp1 =  serializer .validated_data['otp']
                   otp2 =user.otp
                   if(otp1!=otp2): return Response({'error' : "Invalid phone number"},status.HTTP_400_BAD_REQUEST)
                   if(otp1==otp2):
                     try:
                          user.flag=True
                          user.save()
                          return Response({"status":1},status=status.HTTP_200_OK)
                     except Exception as e:
                           return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
               except Exception as e:
                      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                 return Response({'error' : "Invalid phone number"},status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)



class Final_password_set(APIView):
    serializer_class = serializers.New_passSerializer
    def post(self,request):
        serializer  = self.serializer_class(data=request.data)
        if  serializer.is_valid():
            new_pass  = serializer.validated_data['new_pass']
            phone  = serializer.validated_data['phone']
            user = User.objects.filter(mobile_number=phone).exists()
            if user:
               try:
                   user = User.objects.get(mobile_number=phone)
                   if(user.flag is not True):return Response({"error":"you are not allow to change password"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                   if(user.flag is  True):
                     try:
                          user.set_password(new_pass)
                          user.flag=False
                          user.save()
                          return Response({"status":1},status=status.HTTP_200_OK)
                     except Exception as e:
                           return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
               except Exception as e:
                      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                 return Response({'error' : "Invalid phone number"},status.HTTP_400_BAD_REQUEST)
            
            return Response({'status' : 1},status.HTTP_200_OK)
        return Response(serializer.errors)
        



# forget pass end .............X..............







# login_secker

class check_use_login(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.is_authenticated: return Response({"status":1,'user_id' : request.user.id},status=status.HTTP_200_OK)
        else: return Response({"status":0},status=status.HTTP_401_UNAUTHORIZED)
   



# user profile_data

class profele_dta(APIView): ### get or see 
    authentication_classes=[JWTAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user=request.user
        profile_picture_url = request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None
        return JsonResponse({  "email":user.email,'user_id' : user.id,
                         "status":1 ,'user_name':user.name,
                         'phone_number':user. mobile_number,
                         'profile_picture':profile_picture_url,
                         
                         },
                         
                         status=status.HTTP_200_OK)
    




class profele_update(APIView): ### update 
    authentication_classes=[JWTAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers. Profile_updat_Serializer
    parser_classes = (MultiPartParser, FormParser)
    def post(self,request):
        serializer  = self.serializer_class(data=request.data)
        if  serializer.is_valid():
             user=request.user
             profile_picture = request.FILES.get('profile_picture')
             email = serializer.validated_data['email']
             mobile_number = serializer.validated_data['mobile_number']
             name = serializer.validated_data['name']
             try:
                if(profile_picture):user.profile_picture=profile_picture
                if(name):user.name=name
                user.save()
             except Exception as e:pass

             try:
                if mobile_number:
                    if mobile_number==user.mobile_number:pass
                    else:
                        if not User.objects.filter(mobile_number=mobile_number).exists():
                                user.mobile_number=mobile_number
                                user.save()
             except Exception as e:pass

             try:
                if email:
                    if email==user.email:pass
                    else:
                        if not User.objects.filter(email=email).exists():
                                user.email=email
                                user.save()
             except Exception as e:pass
             return Response({"status":1},status=status.HTTP_200_OK)
             


        else:return Response(serializer.errors)
             

        
    
    

