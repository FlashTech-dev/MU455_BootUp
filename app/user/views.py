from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form' : form})


@login_required
def profile(request):
	if request.method == 'POST':
		form = UserUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('index')

	else:
		form = UserUpdateForm(instance=request.user)

	return render(request, 'user_auth/profile.html', {'form': form, 'title': 'Profile'})

def team(request):
    return render(request, 'user/team.html')

def docs(request):
    return render(request, 'user/docs.html')
