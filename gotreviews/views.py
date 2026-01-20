from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from gotreviews.forms import *
from gotreviews.models import *
import csv

# Create your views here.
def go_home(request):
    return render(request, 'inicio.html' )


def show_brotherhoods(request):

    list_brotherhoods = BrotherHoods.objects.all()

    return render(request, 'brotherhoods.html', {'list_brotherhoods': list_brotherhoods})


def do_login(request):

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('go_home')
    else:
        form = LoginForm()


    return render(request, 'login.html', {"form": form})


def do_register(request):


    if request.method == 'POST':
        dataform = RegisterForm(request.POST)

        #validaciones
        if dataform.is_valid():
            user = dataform.save(commit=False)
            user.set_password(dataform.cleaned_data['password'])
            user.save()
            return redirect('do_login')
        else:
            return render(request, 'register.html', {"form": dataform})




    else:
        form = RegisterForm()
        return render(request, 'register.html', {"form": form})



def logout_user(request):
    logout(request)
    return render(request, 'inicio.html')



def admin_panel(request):
    return render(request, 'admin.html')


def data_load(request):


    if request.method == "POST":
        uploaded_file = request.FILES.get('csvFile')

        if not uploaded_file:
            return render(request, 'data_load.html', {'error': 'No se seleccionó ningún archivo.'})

        decoded_file = uploaded_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        code_row = 1

        for row in reader:
            brotherHood = BrotherHoods()
            brotherHood.name = row['Hermandad']
            brotherHood.day = row['Día']
            brotherHood.logo = row['Logo']
            brotherHood.code= code_row
            brotherHood.save()
            code_row += 1






    return render(request, 'data_load.html')



