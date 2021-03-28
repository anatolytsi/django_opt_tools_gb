from django.urls import path

from authapp.views import GeekLoginView, RegisterView, ProfileView, logout

app_name = 'authapp'

urlpatterns = [
    path("login/", GeekLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", logout, name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path('verify/<str:email>/<str:activation_key>/', RegisterView.verify, name='verify'),
]
