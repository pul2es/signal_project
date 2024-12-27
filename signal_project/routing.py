# signal_project/routing.py
from django.urls import re_path
from signal_app import consumers

websocket_urlpatterns = [
    re_path(
        r'ws/signal/(?P<user_id>\w+)/(?P<game_type>\w+)/$',
        consumers.SignalConsumer.as_asgi()
    ),
]

# signal_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signal/', include('signal_app.urls')),
]

# signal_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/current-signal/', views.get_current_signal, name='current_signal'),
    path('api/save-signal/', views.save_user_signal, name='save_signal'),
]