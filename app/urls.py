from os import remove
from unicodedata import name
from django.contrib import admin
from django.urls import include, path

from app import views


urlpatterns = [
    path('',views.index),
    path('signin/',views.signin),
    path('signup/',views.signup),
    path('accounts/', include('django.contrib.auth.urls')),
    path('movie_list/<int:page_number>/',views.movie_list),
    path('movie_detail/<int:id>',views.get_movie_info),
    path('add_to_favorite/<int:id>',views.add_to_favorite,name='add_to_favorite'),
    path('remove_from_favorite/<int:id>',views.remove_from_favorite, name='remove_from_favorite'),
    path('user_favorite',views.get_user_favorite, name='user_favorite'),
    path('footer',views.footer),
    path('dataset/',views.upload_dataset),
    path('api/movies',views.RetriveMovieList.as_view(),name="get_movies_api"),
    path('api/recommended_movie/<int:id>',views.GetMovieRecommendation.as_view(),name="get_movies_recommendation_api"),
    path('api/add_movie',views.CreateMovie.as_view(),name='add_movie'),
  

]