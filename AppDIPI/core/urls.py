from django.urls import path
from .views import home, telas

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('telas', telas, name='telas'),
]