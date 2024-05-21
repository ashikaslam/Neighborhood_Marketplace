from django.urls import path, include


from . import views



#
urlpatterns = [
  
   path('register/',views.RegistrationVies.as_view(),name='register'),
   path('login/',views.Login_api_view.as_view(),name='login'),
   path('logout/',views.Logout.as_view(),name='logout'),
   path('email_varify/',views.email_varify.as_view(),name='email_varify'),
   path('Confirm_otp/',views.Confirm_otp.as_view(),name='Confirm_otp'),
   path('check_use_login/',views.check_use_login.as_view(),name='check_use_login'),
   path('apiLogout/',views.apiLogout.as_view(),name='apiLogout'),

   ##  passwor chage 
   path('chage_pass/',views.change_pass.as_view(),name='chage_pass'),

   ## reset pass urls 
   path('reset_pass_pre/',views.reset_pass_pre.as_view(),name='reset_pass_pre'), # step1
   path('Confirm_otp_pass_change/',views.Confirm_otp_pass_change.as_view(),name='Confirm_otp_pass_change'), # step2
   path('Final_password_set/',views.Final_password_set.as_view(),name='Final_password_set'), #step 3
   ##
  

  # user profile
path('profele_data/',views.profele_dta.as_view(),name='profele_data'),
path('profele_update/',views.profele_update.as_view(),name='profele_update'),

]
