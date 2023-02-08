from django.urls import path
from base.views import *

urlpatterns = [
    path('register', RegistrationView.as_view()),
    path('works', WorkView.as_view()),
]