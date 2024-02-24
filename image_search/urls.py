from django.urls import path
from image_search import views

urlpatterns = [
    path('', view=views.index, name='index'),
    path('login/', view=views.login_function, name='login'),
    path('signup/', view=views.signup_function, name='signup'),
    path('logout/', view=views.logout_function, name='logout'),
    path('file-upload/', view=views.file_upload, name='file_upload'),
    path('file-upload/similarity-search/', view=views.similarity_search, name='similarity_search'),
]
