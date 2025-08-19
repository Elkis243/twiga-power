from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('employment/', employment, name='employment'),
    path('about/', about, name='about'),
]
