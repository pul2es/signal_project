from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/current-signal/', views.get_current_signal, name='current_signal'),
    path('api/save-signal/', views.save_user_signal, name='save_signal'),
]