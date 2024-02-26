from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from zipfile import ZipFile
import os
import shutil
from dashboard.settings import BASE_DIR
from .chromadb_operations import ChromadbOperations


# creating a ChromadbOperations object to insert data
vector_operations = ChromadbOperations()

# Create your views here.


def login_function(request):
    if request.method == 'GET':
        # if authenticated user tries to access the login url again then redirect to home page
        if request.user.is_authenticated:
            return redirect('index')
        form = AuthenticationForm()
        context = {
            "form": form
        }
        return render(request=request, template_name='login.html', context=context)
    else:
        error_message = None
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('index')
        else:
            username = request.POST.get('username')
            all_user = User.objects.all()
            error_message = "No user exit with this username"
            for single_user in all_user:
                if username == single_user.username:
                    error_message = "Password doesn't match"

            context = {
                "form": form,
                "error_message": error_message
            }
            return render(request=request, template_name='login.html', context=context)


def signup_function(request):
    if request.method == 'GET':
        # if authenticated user tries to access the signup url again then redirect to home page
        if request.user.is_authenticated:
            return redirect('index')
        form = UserCreationForm()
        context = {
            'form': form
        }
        return render(request=request, template_name='signup.html', context=context)
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # forming error messages
        error_messages = check_user_credentials({
            'username': request.POST.get('username'),
            'password1': request.POST.get('password1'),
            'password2': request.POST.get('password2')
        })
        context = {
                'form': form,
                'error_messages': error_messages
        }
        if len(error_messages.keys()) == 0:
            if form.is_valid():
                user = form.save()
                if user is not None:
                    return redirect('login')
        else:
            return render(request=request, template_name='signup.html', context=context)


def logout_function(request):
    # clearing previous data in uploads folder
    if len(os.listdir(path=BASE_DIR / 'uploads')) != 0:
        files = os.listdir(path=BASE_DIR / 'uploads')
        for item in files:
            # if it is a file
            if os.path.isfile(BASE_DIR / f'uploads/{item}'):
                os.remove(path=BASE_DIR / f'uploads/{item}')
            
            # if it is a directory
            if os.path.isdir(BASE_DIR / f'uploads/{item}'):
                shutil.rmtree(path=BASE_DIR / f'uploads/{item}')
    
    # cleaning the query results folder
    if len(os.listdir(path=BASE_DIR / f"static/query_results")) != 0:
        image_names = os.listdir(path=BASE_DIR / f"static/query_results")
        for img in image_names:
            os.remove(path=BASE_DIR / f"static/query_results/{img}")

    # cleaning the previous vector data
    vector_operations.delete_vector_storage()

    logout(request=request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    if len(os.listdir(path=BASE_DIR / 'uploads')) != 0:
        return render(request=request, template_name='home.html', context={'current_user': request.user, 'uploaded': True})
    return render(request=request, template_name='home.html', context={'current_user': request.user, 'uploaded': False})


@login_required(login_url='login')
def file_upload(request):
    if request.method == 'GET':
        return render(request=request, template_name='upload.html', context={'current_user': request.user})
    else:
        uploaded_file = request.FILES.getlist('files')[0]
        with open(f"uploads/{uploaded_file.name}", 'wb') as destination_file:
            for chunk in uploaded_file.chunks():
                destination_file.write(chunk)
        destination_file.close()

        # extracting contents from the zip file
        with ZipFile(f'uploads/{uploaded_file.name}', 'r') as zip_ref:
            os.makedirs('uploads/images', exist_ok=True)
            zip_ref.extractall('uploads/images')

        os.remove(f"uploads/{uploaded_file.name}")
        print("[INFO] Data extraction complete")

        vector_operations.create_vector_storage()
        vector_operations.insert_data(BASE_DIR / "uploads/images/")
                
        # switching to search mode based of user choice
        if request.POST['search_mode'] == 'text':
            return render(request=request, template_name='query_with_text.html', context={'current_user': request.user})
        elif request.POST['search_mode'] == 'image':
            return render(request=request, template_name='query_with_image.html', context={'current_user': request.user})
        else:
            return redirect('file_upload')


@login_required(login_url='login')
def similarity_search_text(request):
    if request.method == "POST":
        # running query
        query_text = request.POST['query']
        query_response = vector_operations.query_with_text(query_text=query_text)
        
        # dict to return
        image_paths = []

        # creating a folder for storing query results images
        os.makedirs(name=str(BASE_DIR) + "/static/query_results", exist_ok=True)
        for i in range(len(query_response)):
            # copying the images
            shutil.copy(src=str(BASE_DIR) + '/' + query_response[i], dst=str(BASE_DIR) + "/static/query_results/")
            image_paths.append(query_response[i].split('/')[2])

        return render(request=request, template_name='query_with_text.html', context={'query_response': image_paths, 'current_user': request.user})

    return render(request=request, template_name='query_with_text.html', context={'current_user': request.user})


@login_required(login_url='login')
def similarity_search_image(request):
    if request.method == "POST":
        query_text = request.POST['query']
        return redirect('similarity_search_image')
    else:
        return render(request=request, template_name='query_with_image.html', context={'current_user': request.user})


def check_user_credentials(user_info):
    username = user_info['username']
    password1 = user_info['password1']
    password2 = user_info['password2']

    all_user = User.objects.all()
    error_messages = {}
    for single_user in all_user:
        if username == single_user.username:
            error_messages['username_error_msg'] = "Username is taken"

    if password1 != password2:
        error_messages['password_error_msg'] = "Password doesn't match"
    else:
        if len(password1) < 8:
            error_messages['password_error_msg'] = "Minimum password length is 8"
    
    return error_messages