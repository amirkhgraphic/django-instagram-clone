from django.urls import path

from user.api import Signup, Login, TestToken

urlpatterns = [
    path('signup/', Signup.as_view(), name='sign-up'),
    path('login/', Login.as_view(), name='log-in'),
    path('testtoken/', TestToken.as_view(), name='test-token'),
]
