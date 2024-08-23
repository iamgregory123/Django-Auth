from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'auth/register.html', {'form': form})  
    else:
        form = UserCreationForm()
        return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password) 

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'auth/login.html', {'form': form, 'error': 'Invalid login credentials'})  

        else:
            return render(request, 'auth/login.html', {'form': form})  
    else:
        form = AuthenticationForm()
        return render(request, 'auth/login.html', {'form': form})

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'auth/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')
