from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages

from budgie.forms import LoginForm

def index(request):
    if request.user.is_active:
        return redirect('home')
    else:
        return redirect('user_login')

def user_login(request):
    template = 'login.html'
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        next_page = request.GET.get('next', None)
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if next_page:
                        return redirect(next_page)
                    else:
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
    return redirect('user_login')
