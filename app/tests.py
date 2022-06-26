from turtle import title
from django.test import TestCase
from django.contrib.auth.models import User

from .models  import Movie

class MovieTestCase(TestCase):
    def setUp(self):
        movie = Movie.objects.create(title="Batman",budget=10000)

        user1 = User.objects.create_user(username='john1',email='john1@gmail.com',password='test@123')

        user2 = User.objects.create_user(username='john2',email='john2@gmail.com',password='test@123')

        movie.favorite.add(user1)
        movie.favorite.add(user2)

    def test_movie_name(self):
        batman = Movie.objects.get(title="Batman")
        self.assertEqual(batman.title,"Batman")

    def test_budget_in_yen(self):
        batman = Movie.objects.get(title="Batman")
        self.assertEqual(batman.get_budget_in_yen(),1220000) 

    def test_movie_users(self):
        batman=Movie.objects.get(title="Batman")
        self.assertEqual(batman.favorite.count(), 2)

    

