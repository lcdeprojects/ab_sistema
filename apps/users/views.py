from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

def redirect_to_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('users:login')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Você saiu do sistema com sucesso.")
    return redirect('users:login')

@login_required
@user_passes_test(lambda u: u.is_staff)
def register_user_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Usuário {form.cleaned_data['username']} criado com sucesso!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

