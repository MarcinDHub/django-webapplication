from django.db import models
from django.db.models import CharField, ForeignKey, DateField, ManyToManyField, BooleanField, DateTimeField, DurationField, EmailField, IntegerField, TextField, OneToOneField
from django.contrib.auth.models import User
import datetime


# Create your models here.
class City(models.Model):
	name = CharField(max_length=32)
	region = CharField(max_length=32)

	def __str__(self):
		return self.name


class Company(models.Model):
	name = CharField(max_length=32)
	city = ForeignKey(City, on_delete=models.SET_NULL, null=True)
	signed = BooleanField(default=0)
	signed_date = DateField
	email = EmailField(max_length=32, null=True)
	phonenumber = CharField(max_length=32)
	nip = CharField(max_length=32)
	adress = CharField(max_length=100)


	def __str__(self):
		return self.name


class MeetingStatus(models.Model):
	name = CharField(max_length=100)

	def __str__(self):
		return self.name


class Meeting(models.Model):
	date = DateTimeField()
	company = ForeignKey(Company, on_delete=models.SET_NULL, null=True)
	city = ForeignKey(City, on_delete=models.SET_NULL, null=True)
	leader = ForeignKey(User, related_name='leaderofmeeting', on_delete=models.SET_NULL, null=True)
	trader_1 = ForeignKey(User, related_name='trader1ofmeeting', on_delete=models.SET_NULL, null=True)
	trader_2 = ForeignKey(User, related_name='trader2ofmeeting', on_delete=models.SET_NULL, null=True)
	status = ForeignKey(MeetingStatus,  on_delete=models.SET_NULL, null=True)

	class Meta:
		verbose_name = 'Spotkanie'
		verbose_name_plural = 'Spotkania'


	def __str__(self):
		return str(self.date) + " / " + str(self.company) + " / " + str(self.city) + "  ---  " + str(self.leader) + " i " + str(self.trader_1)





class PhoneCalls(models.Model):
	date = DateTimeField()
	employee = ForeignKey(User, on_delete=models.SET_NULL, null=True)
	company = ForeignKey(Company, on_delete=models.SET_NULL, null=True)
	description = TextField(max_length=1024, null=True, default=" ")

	class Meta:
		verbose_name = 'Połączenie telefoniczne'
		verbose_name_plural = 'Połączenia telefoniczne'

	def __str__(self):
		return str(self.date) + " " + str(self.employee)


class Post(models.Model):
	title = CharField(max_length=100)
	author = ForeignKey(User, on_delete=models.SET_NULL, null=True)
	date = DateField()
	content = CharField(max_length=2000)

	def __str__(self):
		return self.title


class UserNorm(models.Model):
	employee = ForeignKey(User, on_delete=models.SET_NULL, null=True, unique=True)
	meetings_month_norm = IntegerField()
	phonecalls_week_norm = IntegerField()
	phonecalls_month_norm = IntegerField()
	test = CharField(max_length=100)
	# avatar = models.ImageField()

	class Meta:
		verbose_name = 'Statystyki użytkownika'
		verbose_name_plural = 'Statystyki użytkowników'

	def __str__(self):
		return str(self.employee)

class ActivityType(models.Model):
	name = CharField(max_length=100)

	def __str__(self):
		return self.name

class Activity(models.Model):
	employee = ForeignKey(User, on_delete=models.SET_NULL, null=True)
	date = DateTimeField(null=True)
	typeof = ForeignKey(ActivityType, on_delete=models.SET_NULL, null=True)
	company = ForeignKey(Company, on_delete=models.SET_NULL, null=True)
	description = TextField(max_length=1024, null=True, default=" ")



	class Meta:
		verbose_name = 'Aktywność'
		verbose_name_plural = 'Aktywności'


	def __str__(self):
		return self.employee

		
