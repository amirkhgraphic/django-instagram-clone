from django.urls import path
from .views import LogCreateAPIView

urlpatterns = [
    path('create/', LogCreateAPIView.as_view(), name='create'),
]
