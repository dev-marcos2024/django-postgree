from django.contrib import admin
from django.urls import path
from core.views import index, produto, contato

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', index, name='index'),
    path('produto/', produto, name='produto'),
    path('contato/', contato, name='contato'),
]