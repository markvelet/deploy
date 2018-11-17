from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
	return render(request, 'login_app/index.html')

def register(request):

	errors = User.objects.validations(request.POST)
	if len(errors):
		for tag, error in errors.items():
			messages.error(request, error, extra_tags = tag)
			
		return redirect('/')
	else:
		user = User.objects.create(
			first_name=request.POST['first'],
			last_name= request.POST['last'],
			email=request.POST['email'],
			passhash = bcrypt.hashpw(request.POST['pass1'].encode(),bcrypt.gensalt())
			)
		user.save()
		request.session['id'] = user.id
		request.session['firstname'] = user.first_name
		messages.success(request, 'You successfully registered!')
		return redirect('/success')

	return redirect('/success') 
def login(request):
	errors2 = User.objects.login(request.POST)

	if len(errors2):
		for key, value in errors2.items():
			messages.error(request, value, extra_tags = key)
		return redirect('/')

	else:
		userlogin = User.objects.get(email=request.POST['email'])
		if bcrypt.checkpw(request.POST['pass1'].encode(),userlogin.passhash.encode()):
			request.session['email'] = userlogin.email
			request.session['firstname'] = userlogin.first_name
			request.session['id'] = userlogin.id
			request.session['messages'] = "Logged in"
			messages.success(request, 'logged in')
			return redirect('/success')
		else:
			messages.info(request, 'Incorrect Email/Password')
			return redirect('/')


	return redirect('/')
def success(request):
	if 'id' not in request.session:
		messages.success(request, 'Cannot bypass lol')
		return redirect('/')
	currentUser = User.objects.get(id=request.session['id'])
	context = {'users' : currentUser}
	return render(request, 'login_app/success.html',context)

def logout(request):
	if 'logid' in request.session:
		request.session.clear()
		messages.success(request, 'logged out successfully.')
		return redirect('/')
	return redirect('/success')
	# return redirect('/')
