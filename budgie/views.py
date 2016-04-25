from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

from budgie.forms import LoginForm

def login(request):
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
                    return redirect('index')
                else:
                    messages.error(request, 'Your account has been disabled.')
            else:
                messages.error(request, 'Invalid login credentials.')

            # Maybe not return this one?
            # return request
    else:
        context['form'] = LoginForm()

    return render(request, template, context)
