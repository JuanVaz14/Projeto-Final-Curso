from django.urls import path
from . import views

app_name = 'links'

urlpatterns = [
    path('', views.home_view, name='home'),
    # Adicione mais URLs aqui conforme for desenvolvendo o app 'links'
]
