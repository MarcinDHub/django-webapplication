from django import forms
from blog.models import Meeting, Company, PhoneCalls, Activity, ActivityType
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# from bootstrap_datepicker_plus import DatePickerInput

class DateInput(forms.DateInput):
	input_type = 'date'


class PostForm(forms.ModelForm):
	company = forms.ModelChoiceField(
				queryset=Company.objects.all().order_by('name'), 
				label="Klient", 
				widget=forms.Select(attrs={'class': 'form-control'}))
	trader_1 = forms.ModelChoiceField(
				queryset=User.objects.filter(groups__name='Handlowiec').order_by('first_name'),
				label="Partner",
				widget=forms.Select(attrs={'class': 'form-control'}))



	# date =  forms.TextInput(
	# 			widget=forms.TextInput(attrs={'class': 'form-control'}))

	class Meta:
		model = Meeting
		fields = ('date', 'company', 'trader_1')

		widgets = {
			'date':forms.TextInput(attrs={
            		'class': 'form-control',
            		'autocomplete': 'off',
            		'id': 'm_date',
            		'placeholder': 'wybierz datę'})
		}



class PlanPhoneCallForm(forms.ModelForm):
	company = forms.ModelChoiceField(
				queryset=Company.objects.all().order_by('name'), 
				label="Klient", 
				widget=forms.Select(attrs={'class': 'form-control'}))

	description = forms.CharField(widget=forms.Textarea(),
								  label="Opis rozmowy")

	# date = forms.DateField(
 #        widget=DatePickerInput(format='%m/%d/%Y')
 #    )
	# date = forms.widgets.DateTimeInput(attrs={'type':'date'})
	class Meta:
		model = PhoneCalls
		fields = ('date', 'company', 'description',  )

		widgets = {
			'date':forms.TextInput(attrs={
            		'class': 'form-control',
            		'id': 'pc_date',
            		'autocomplete': 'off',
            		'placeholder': 'wybierz datę'})
		}



class ActivityForm(forms.ModelForm):
	
	typeof = forms.ModelChoiceField(
			queryset=ActivityType.objects.all(),
			label="Aktywność",
			widget=forms.Select(attrs={'class': 'form-control'}))


	company = forms.ModelChoiceField(
			queryset=Company.objects.all(),
			label="Firma",
			widget=forms.Select(attrs={'class': 'form-control'}))

	description = forms.CharField(widget=forms.Textarea(),
								  label="Komentarz")

	class Meta:
		model = Activity
		fields = ('date', 'typeof', 'company', 'description')

		widgets = {
			'date':forms.TextInput(attrs={
            		'class': 'form-control',
            		'id': 'a_date',
            		'autocomplete': 'off',
            		'placeholder': 'wybierz datę'})
		}

