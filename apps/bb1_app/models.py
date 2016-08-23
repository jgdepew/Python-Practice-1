from __future__ import unicode_literals
import re
from django.db import models
from django.contrib import messages
import bcrypt
from datetime import datetime

# Create your models here.

class ValidationManager(models.Manager):
	def UserValidation(self, request, form_info):
		errors = 0
		if 'password2' in form_info:
			name = form_info['name']
			username = form_info['username']
			password1 = form_info['password1']
			password2 = form_info['password2']

			if len(username)<3:
				messages.error(request, 'Not a valid username.')
				errors += 1
			elif User.objects.filter(username=username):
				messages.error(request, 'Username already in use.')
				errors += 1

			if len(name) < 3:
				messages.error(request, 'Name are not valid.')
				errors += 1

			if password1 != password2:
				messages.error(request, 'Passwords do not match.')
				errors += 1			
			elif len(password1)<8:
				messages.error(request, 'Not a valid password.')
				errors += 1			

			if errors > 0:
				return False
			else:
				password = str(password1)
				hashed = bcrypt.hashpw(password, bcrypt.gensalt())
				User.objects.create(name=name, username=username, password=hashed)
				user = User.objects.get(username=username)
				request.session['name'] = user.name
				request.session['id'] = user.id
				request.session['username'] = user.username			
				return True
		else:
			username = form_info['username']
			password = form_info['password']
			if len(User.objects.filter(username=username))<1:
				messages.error(request, 'Invalid login information.')
				return False
			user = User.objects.get(username=username)
			password_entered = password.encode()
			hashed_entered = bcrypt.hashpw(password_entered, bcrypt.gensalt())
			if username == user.username and bcrypt.hashpw(password_entered, user.password.encode()) == user.password:
				request.session['name'] = user.name
				request.session['id'] = user.id
				request.session['username'] = user.username
				return True
			else: 
				messages.error(request, 'Password incorrect.')
				return False
	def TripValidation(self, request, form_info):
		errors = 0
		destination = form_info['destination']
		description = form_info['description']
		user = User.objects.get(id=request.session['id'])
		date_start = form_info['date_start']
		date_end = form_info['date_end']
		start = date_start.encode()
		end = date_end.encode()
		if len(destination) < 2:
			errors += 1
			messages.error(request, 'Not a valid destination.')
		if len(description) < 1:
			errors += 1
			messages.error(request, 'You forgot to describe your travel plans!')
		if len(str(start)) < 1:
			errors += 1
			messages.error(request, 'Start date not entered.')
		if len(str(end)) < 1:
			errors += 1
			messages.error(request, 'End date not entered.')

		if date_start and date_end:
			date_end = datetime.strptime(date_end, "%Y-%m-%d")
			date_start = datetime.strptime(date_start, "%Y-%m-%d")
			if datetime.now() >= date_start:
				errors += 1
				messages.error(request, 'Start date is in the past')
			if date_start >= date_end:
				errors += 1
				messages.error(request, 'End date must be after start date.') 
		if errors > 0:
			return False
		else:
			Trip.objects.create(destination=destination, description=description, date_start=date_start, date_end=date_end, planned_by=user)
	def Add_User_to_Trip(self, request, id, form_info):
		user = User.objects.get(id=request.session['id'])
		trip = self.get(id=id)
		trip.users.add(user)
		trip.save()


class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ValidationManager()

class Trip(models.Model):
	destination = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	date_start = models.CharField(max_length=255)
	date_end = models.CharField(max_length=255)
	planned_by = models.ForeignKey(User, related_name='planned_by')
	users = models.ManyToManyField(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ValidationManager()