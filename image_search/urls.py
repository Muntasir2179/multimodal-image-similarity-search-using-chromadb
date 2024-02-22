from django.urls import path
from image_search import views

urlpatterns = [
    path('', view=views.home, name='home'),
]
