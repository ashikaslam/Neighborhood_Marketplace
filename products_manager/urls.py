from django.urls import path, include
from . import views
#
urlpatterns = [
  
   path('create_sell_post/',views.create_sell_post.as_view(),name='create_sell_post'),
   path('RecentPost/',views.RecentPost.as_view(),name='RecentPost'),
   path('my_post/',views.my_post.as_view(),name='my_post'),
   path('delete_my_post/',views.delete_my_post.as_view(),name='delete_my_post'),
   path('update_sell_post/',views.update_sell_post.as_view(),name='update_sell_post'),
   
 

]
