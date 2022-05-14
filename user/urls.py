from django.contrib.auth.decorators import login_required
from django.urls import path

from user.views import LogoutView, RegisterView, LoginView

app_name = 'user'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
]
