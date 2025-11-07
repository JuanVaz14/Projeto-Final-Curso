from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    # Usa o template base/em_construcao.html que herda o layout bonito de sidebar
    return render(request, 'base/em_construcao.html', {'app_name': 'Empresas'})
