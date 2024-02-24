from django.urls import path
from image_search import views

urlpatterns = [
    path('', view=views.index, name='index'),
]
