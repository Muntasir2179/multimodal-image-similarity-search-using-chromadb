from django.shortcuts import render, HttpResponse

# Create your views here.

def home(request):
    return HttpResponse('<p>This is Home page</p>')