import math
from multiprocessing import context
import re
import pandas as pd
from django.shortcuts import redirect, render

from django.db import transaction

from app.forms import MovieForm, ReviewForm, UploadFrom
from .ml import get_recommendation_for_movie
from .models import Genre, Movie, Review

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate,login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieSerializer

# Create your views here.


def index(request):
    movies = Movie.objects.all()
    return render(request, 'index.html',{'movies': movies})

def signup(request):
    return render(request,"signup.html")

def logout(request):
    pass

def movie_list(request, page_number):
    page_size = 3
    if page_number < 1:
        page_number = 1
    movie_count = Movie.objects.count()
    last_page = math.ceil(movie_count/page_size)
    pagination ={
        'previous_page':page_number-1,
        'current_page':page_number,
        'next_page':page_number + 1,
        'last_page':last_page 
    }
    movies = Movie.objects.all()[(page_number-1)*page_size:page_number*page_size]
    return render(request, 'movie_list.html',
     {'movies': movies,
     'pagination':pagination})


def get_movie_info(request, id):
    try:
        review_form = ReviewForm()
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.movie_id = id
                review.user_id=request.user.id
                review.save()

        movie = Movie.objects.get(id=id)
        reviews = Review.objects.filter(movie=movie).order_by('-created_at')[0:4]

        
        context ={
            'is_favourite':False
        }
        print(id)
        movie_ids =get_recommendation_for_movie(id)


        recommended_movies = Movie.objects.filter(id__in=movie_ids)
        if movie.favorite.filter(pk=request.user.pk).exists():
            context['is_favourite']= True

        return render(request, 'movie_detail.html',
        {'movie': movie, 
        'context':context,
        'review_form': review_form,
        'reviews':reviews,
        'recommended_movies':recommended_movies
        })
    except Movie.DoesNotExist:
        return render(request, '404.html')


   

def post_movie(request):
    form = MovieForm()

    if request.method == "POST":
        movie_form = MovieForm(request.POST)

        if movie_form.is_valid():
            movie_form.save()

            return redirect('/movies/')

    return render(request, 'post_movie.html', {'form': form})


def signin(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'])
            login(request,user)
            return redirect('/')

    return render(request,'signin.html',{'form':form})

def signup(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('/')

    return render(request, 'signup.html', {'form': form})

def add_to_favorite(request,id):
    movie =  Movie.objects.get(id=id);
    movie.favorite.add(request.user)
    return redirect('/movie_detail/{0}'.format(id))

def remove_from_favorite(request,id):
    movie = Movie.objects.get(id=id)
    movie.favorite.remove(request.user)
    return redirect('/movie_detail/{0}'.format(id))\

def get_user_favorite(request):
    movies = request.user.favorite.all()
    return render(request,'user_favorite.html',{'movies':movies})

def footer(request):
    return render(request,"footer.html")
    

def upload_dataset(request):
    file_form = UploadFrom()
    error_message ={}

    if request.method == "POST":
        file_form = UploadFrom(request.POST,request.FILES)
        try:
            if file_form.is_valid():
                dataset = pd.read_csv(request.FILES['file'])
                new_movies_list =[]
                dataset['budget'] = dataset['budget'].fillna(0)
                with transaction.atomic():
                    for index, row in dataset.iterrows():
                        movie = Movie(
                            title=row['title'],
                            budget=row['budget'],
                            genres = row['genres'],
                            keywords = row['keywords'],
                            overview =row['overview'],
                            tagline=row['tagline'],
                            cast=row['cast'],
                            director = row['director']
                        )
                        new_movies_list.append(movie)
                Movie.objects.bulk_create(new_movies_list)
            return redirect('/dataset')
        except Exception as e:
            print(e)
            error_message['error'] = e
    return render(request,'upload_dataset.html',{'form':file_form,'error_message':error_message})

class RetriveMovieList(APIView):
    def get(self, request):
        movies = Movie.objects.all()[0:10]
        serializer = MovieSerializer(movies,many= True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class GetMovieRecommendation(APIView):
    def get(self,request,id):
        movie_ids = get_recommendation_for_movie(id)

        recommended_movies = Movie.objects.filter(id__in=movie_ids)
        serializers = MovieSerializer(recommended_movies,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK) 

class CreateMovie(APIView):
    def post(self,request):
        serializers = MovieSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

