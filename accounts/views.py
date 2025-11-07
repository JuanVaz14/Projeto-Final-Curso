from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login 
from .forms import UsuarioCreationForm 
from django.contrib.auth.views import LoginView

# View de Login customizada (opcional, mas mantém o fluxo)
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

# Home pública
def home_view(request):
    return render(request, 'base/home.html', {'titulo': 'Bem-vindo à Intranet ACJogos-RJ'})

# Dashboard (acesso após login)
@login_required
def dashboard_view(request):
    return render(request, 'base/dashboard.html', {'titulo': 'Dashboard'})


# View de Registro
def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('accounts:dashboard')
    else:
        form = UsuarioCreationForm()
    
    context = {'form': form, 'titulo': 'Criar Conta'}
    return render(request, 'accounts/registrar.html', context)
