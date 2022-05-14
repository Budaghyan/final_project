from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.views import LoginView as BaseLoginView
from user.forms import RegisterForm
from user.models import User
from django.contrib.auth import login


class RegisterView(View):
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            return redirect('/quotes')
        print(register_form.errors)

        return render(request, 'user/register.html', {'form': register_form})

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'user/register.html', {'form': register_form})


# class LoginView(View):
#     def post(self, request):
#         username = request.POST['username']
#         password = request.POST['password']
#         print(username)
#         print(password)
#         user = authenticate(username=username, password=password)
#         print(user)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#
#                 return HttpResponseRedirect('/quotes')
#             else:
#                 return HttpResponse("Inactive user.")
#         else:
#             return HttpResponseRedirect('/user/login')
#
#     def get(self, request):
#         return render(request, "user/login.html")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/quotes')
