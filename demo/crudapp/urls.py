from django.urls import path,include
from .views import Views
urlpatterns = [
    path('',view=Views.as_view(),name='home')
]