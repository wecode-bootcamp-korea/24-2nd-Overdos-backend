from django.urls import path
from .views import KakaoLoginView, LoginView, SignupView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/login', LoginView.as_view()),
    path('/kakaologin', KakaoLoginView.as_view()),
]