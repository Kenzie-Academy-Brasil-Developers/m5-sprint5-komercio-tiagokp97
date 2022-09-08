from django.urls import path

from . import views

urlpatterns = [
    path("accounts/", views.ListCreateAccountView.as_view()),
    path("accounts/<pk>/", views.UpdateAccountView.as_view()),
    path("accounts/<pk>/management/", views.UpdateAccountViewAdmin.as_view()),
    path("accounts/newest/<int:num>/", views.ListAccountView.as_view()),
    path("login/", views.LoginView.as_view()),
]
