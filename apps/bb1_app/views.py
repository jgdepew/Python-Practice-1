from django.shortcuts import render, redirect, reverse
from .models import User, Trip
# Create your views here.

# loging and registration validation 
def validation(request):
	if request.method == 'POST':
		return process_validation(request)
	return render(request, 'bb1_app/validation.html')

# process validation
def process_validation(request):
	if User.objects.UserValidation(request, request.POST):
		User.objects.UserValidation(request, request.POST)
		return redirect(reverse('belt:index'))
	else: 
		return redirect(reverse('belt:validation'))

# SEMI-REST index html and create
def index(request):
	if request.method == 'POST':
		return create(request)
	context = {
		'user': User.objects.get(id=request.session['id']),
		'trips': Trip.objects.all()
	}
	return render(request, 'bb1_app/index.html', context)

# new html
def new(request):
	return render(request, 'bb1_app/new.html')

# create: receives from INDEX
def create(request):
	if Trip.objects.TripValidation(request, request.POST)==False:
		return redirect(reverse('belt:new'))
	return redirect(reverse('belt:index'))

# SEMI-REST show html and update
def show(request, id):
	if request.method == 'POST':
		return update(request, id)
	context = {
		'trip': Trip.objects.get(id=id),
		'users': User.objects.filter(trip=Trip.objects.get(id=id)),
	}
	return render(request, 'bb1_app/show.html', context)

# edit html
def edit(request, id):
	return render(request, 'bb1_app/edit.html')

# update: receives from SHOW 
def update(request, id):
	Trip.objects.Add_User_to_Trip(request, id, request.POST)
	return redirect(reverse('belt:show', kwargs={'id': id}))

def destroy(request, id):
	Trip.objects.get(id=id).delete()
	return redirect(reverse('belt:index'))

#logout
def logout(request):
	for key in request.session.keys():
		del request.session[key]
	return redirect(reverse('belt:validation'))