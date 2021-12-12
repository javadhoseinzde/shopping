from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.urls.base import reverse, reverse_lazy
from .forms import  SighUpForm, LoginForm, MyPasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import ugettext as _

def signup(request):
	if request.method == 'POST':
		form = SighUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('shopping:home')
	else:
		form = SighUpForm()
	return render(request, 'signup.html', {'form': form})



def signin(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request,
								username = cd['username'],
								password=cd['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					redirect('shopping:home')
			redirect('shopping:home')
	else:
		form = LoginForm()
		return render(request, 'signin.html', {'form': form})

def PasswordChangeView(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Profile updated '\
									  'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        form = MyPasswordChangeForm(request.user)
    return render(request, "change_pass.html", {
        'form': form
    })

