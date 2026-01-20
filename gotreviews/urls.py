from django.contrib import admin
from django.urls import path, include

from gotreviews.views import *

urlpatterns = [
    path('', go_home, name='go_home'),
    path('characters/', show_characters, name='characters'),
    path('login/', do_login, name='do_login'),
    path('register/', do_register, name='do_register'),
    path('logout/', logout_user, name='logout_user'),
    path('admin_panel/', admin_panel, name='go_admin_panel'),
    path('data_load/', data_load, name='go_data_load'),

]
