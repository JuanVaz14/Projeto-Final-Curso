from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UsuarioCreationForm

def home_view(request):
    return render(request, 'base/home.html')

@login_required
def dashboard_view(request):
    return render(request, 'base/dashboard.html')

def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = UsuarioCreationForm()
    return render(request, 'accounts/registrar.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')
