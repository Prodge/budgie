from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages

from budgie.forms import LoginForm

def user_login(request):
    template = 'login.html'
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Your account has been disabled.')
        messages.error(request, 'Invalid login credentials.')
        context['form'] = LoginForm(request.POST)
    else:
        context['form'] = LoginForm()

    return render(request, template, context)

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('login')
