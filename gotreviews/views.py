import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from gotreviews.forms import *
from gotreviews.models import *
import csv


# Create your views here.
def go_home(request):
    return render(request, 'inicio.html')


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

        # validaciones
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
            brotherHood.code = code_row
            brotherHood.save()
            code_row += 1

    return render(request, 'data_load.html')


def show_categories(request):
    categories = Category.objects.all()
    return render(request, 'ranking_categories.html', {'categories': categories})


def go_rankings(request, id):
    category = Category.objects.get(code=id)

    list_brotherhoods = BrotherHoods.objects.filter(code__in=category.brotherhoods)
    return render(request, 'ranking.html', {
        'items': list_brotherhoods,
        'category_code': category.code,
        'category_size': len(category.brotherhoods),
    })


def categories(request):
    categories = Category.objects.all()
    list_brotherhoods = BrotherHoods.objects.all()


    if request.method == "POST":
        category = Category()
        category.name = request.POST.get('name')
        category.logo = request.POST.get('logo')
        category.description = request.POST.get('description')

        last_category = Category.objects.order_by('code').last()
        last_code = last_category.code if last_category else 0
        category.code = last_code + 1

        brotherhoods = json.loads(request.POST.get('brotherhoods'))
        brotherhoods_int = [int(x) for x in brotherhoods]
        category.brotherhoods = brotherhoods_int

        category.save()

        return redirect('go_categories')

    return render(request, 'categories.html',
                  {
                      'categories': categories,
                      'brotherhoods': list_brotherhoods
                  })


def save_top(request):
    order = request.POST.get('order')
    order_list = json.loads(order)
    category_size = request.POST.get('category_size')

    if len(order_list) != category_size:
        ranking = Ranking()
        ranking.rankinDate = timezone.now()
        ranking.user = request.user
        ranking.categoryCode = request.POST.get('category_code')
        ranking.rankinList = [order_list]
        ranking.save()

    return redirect('go_home')


def delete_category(request, code):
    Category.objects.filter(code=code).delete()
    return redirect('go_categories')