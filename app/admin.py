from django.contrib import admin
from .models import Genre, Movie, Review




class MovieAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'budget','genres')

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name','description')


# Register your models here.
admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre,GenreAdmin)
admin.site.register(Review)
