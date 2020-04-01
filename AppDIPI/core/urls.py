from django.urls import path
from .views import home, telas, adminsite

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('admsite', adminsite, name='adminsite'),
    path('telas', telas, name='telas'),
]