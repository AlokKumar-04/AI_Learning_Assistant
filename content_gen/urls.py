from django.urls import path
from .views import index

app_name = 'content_gen'

urlpatterns = [
    path('', index, name='index'),
]
