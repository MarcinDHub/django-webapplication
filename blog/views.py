from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Company, City, Meeting, UserNorm, PhoneCalls, Activity
from django.db.models import Q
from blog.forms import PostForm, PlanPhoneCallForm, ActivityForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta
from django.views.decorators.http import require_POST



def scheduler(request):

	a_form = ActivityForm()
	data = Activity.objects.all().order_by('date')

	if request.method == "POST":
		form = ActivityForm(request.POST)

		if form.is_valid():

			instance = form.save(commit=False)
			print(instance)
			instance.employee_id = request.user.id
			instance.save()	

	context = {
		'a_form': a_form,
		'data': data,
	}

	return render(request, 'blog/scheduler.html', context)


def calendar(request):
	today = datetime.now()
	weekday = today.isoweekday()
	start = datetime.now()-timedelta(days=weekday-1)
	first_week = []
	second_week = []
	records_first_week = []
	records_second_week = []

	for i in range(0,14):
		x = ""
		x = Meeting.objects.filter(Q(leader__id=request.user.id) | Q(trader_1__id=request.user.id),
								   date__year=start.year,
								   date__month=start.month,
								   date__day=start.day).order_by('date')
		
		if i < 7:
			records_first_week.append(x)
		else:
			records_second_week.append(x)

		start = start + timedelta(days=1)

	start = datetime.now()-timedelta(days=weekday-1)
	for i in range(0,14):
		if i < 7:
			first_week.append(start+timedelta(days=i))
			records_first_week[i].dd = start+timedelta(days=i)

		else:
			second_week.append(start+timedelta(days=i))
			# records_second_week[i].d = start+timedelta(days=i)
	form = PostForm()

	if request.method == "POST":

		form = PostForm(request.POST)
		if form.is_valid():
			print("is valid")
			# city = form.cleaned_data['company']
			# print(city)
			instance = form.save(commit=False)
			instance.city = instance.company.city
			instance.leader_id = request.user.id
			instance.save()
			return redirect("blog-calendar")

	context = {
		'first_week': first_week,
		'second_week': second_week,
		'records_first_week': records_first_week,
		'records_second_week': records_second_week,
		'today': datetime.now() , 
		'cities': City.objects.all().order_by('name'),
		'employee': User.objects.all().exclude(id = request.user.id).order_by('first_name'),
		'form': form,
	}



	return render(request, 'blog/calendar.html', context)

# @require_POST
# def addTodo(request):
# 	todoform = PostForm(request.POST)
# 	print("here")
# 	if todoform.is_valid():
# 		new_todo = todoform.save()
# 		print("form saved")

# 	return redirect('blog-desktop')


def search(request):
	if request.method == "GET":
	# if query:
		query = request.GET.get("q")

		results_company = Company.objects.filter(name__contains=query).order_by('name')
		results_person = User.objects.filter(Q(first_name__contains=query) | Q(last_name__contains=query))
		print(results_company)
		print(results_person)
		context = {
			'query': query, 
			'results_person': results_person,
			'results_company': results_company,
		}
		return render(request, "blog/search_results.html", context)



def meeting_edit(request):
	if request.method == "GET":
		if 'd' in request.GET:
			print("dddddddddddddd")
			query = request.GET.get("d")

			item = Meeting.objects.get(id=query)
			print(item)
			item.status = 1
			item.save()

		elif 'p' in request.GET:	
			pass

		elif 'c' in request.GET:	
			query = request.GET.get("c")
			item = Meeting.objects.get(id=query)
			item.status = 2
			item.save()

		return redirect('blog-desktop')


def home(request):
	return render(request, 'blog/home.html')


def mystats(request):

	def color(pct):
		if pct < 50:
			return '-danger'
		elif pct < 100:
			return '-warning'
		else:
			return '-success'


	title = "pulpit"

	# All meetings for current user
	m_all = Meeting.objects.filter(Q(leader__id=request.user.id) | Q(trader_1__id=request.user.id)).order_by('date')
	m_planned = m_all.filter(status_id=1, date__gt=datetime.now())
	m_done = m_all.filter(status_id=2)

	# Monthly meetings
	mm_done = m_all.filter(status_id=2, date__month=datetime.now().month)
	mm_norm = UserNorm.objects.get(employee_id=request.user.id).meetings_month_norm
	mm_pct = int(100*len(mm_done)/mm_norm)
	m_to_acc = m_all.filter(status_id=1, date__lte=datetime.now())

	# All phonecalls for current user
	pc_all = PhoneCalls.objects.filter(employee_id=request.user.id)

	# Monthly phonecalls
	pcm_done = pc_all.filter(date__month=datetime.now().month)
	pcm_norm = UserNorm.objects.get(employee_id=request.user.id).phonecalls_month_norm
	pcm_pct = int(100*len(pcm_done)/pcm_norm)

	# Weekly phonecalls
	pcw_done = pc_all.filter(date__week=date.today().isocalendar()[1])
	pcw_norm = UserNorm.objects.get(employee_id=request.user.id).phonecalls_week_norm
	pcw_pct = int(100*len(pcw_done)/pcw_norm)

	m_form = PostForm()
	pc_form = PlanPhoneCallForm()


	if request.method == "POST":
		
		m_form = PostForm(request.POST)
		pc_form = PlanPhoneCallForm(request.POST)

		if m_form.is_valid():
			instance = m_form.save(commit=False)
			instance.city = instance.company.city
			instance.leader_id = request.user.id
			instance.status_id = 1
			instance.save()
			return redirect('blog-desktop')

		if pc_form.is_valid():
			print("ok")
			instance = pc_form.save(commit=False)
			instance.employee_id = request.user.id
			instance.save()
			return redirect('blog-desktop')



	context = {
		'title': title,
		'm_planned': m_planned,
		'm_to_acc': m_to_acc,
		'm_done_last_5': m_done[:5],
		'mm_done_len': len(mm_done),
		'mm_norm': mm_norm,
		'mm_pct': mm_pct,
		'mm_color': color(mm_pct),
		'pcw_norm': pcw_norm,
		'pcw_done_len': len(pcw_done),
		'pcw_pct': pcw_pct,
		'pcw_color': color(pcw_pct),
		'pcm_norm': pcm_norm,
		'pcm_done_len': len(pcm_done),
		'pcm_pct': pcm_pct,
		'pcm_color': color(pcm_pct),
		'm_form': m_form,
		'pc_form': pc_form,
	}

	return render(request, 'blog/mystats.html', context)


def meetings(request):
	if request.user.is_staff:
		respond_meetings = Meeting.objects.all().order_by('-date')
	else:
		respond_meetings = Meeting.objects.filter(Q(leader__id=request.user.id) | Q(trader_1__id=request.user.id))

	context = {
		'meetings_all': respond_meetings,
		'user_list': User.objects.all(),
	}
	return render(request, 'blog/meetings.html', context)


def phonecalls(request):
	if request.user.is_staff:
		respond = PhoneCalls.objects.all().order_by('-date')
	else:
		respond = PhoneCalls.objects.filter(employee=request.user.id).order_by('-date')

	context = {
		'phonecalls_all': respond,
		'user_list': User.objects.all(),
	}
	return render(request, 'blog/phonecalls.html', context)


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			# username = form.cleaned_data.get('username')
			# password = form.cleaned_data.get('password')
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"Zalogowano jako {username}")
				return redirect("blog-home")
			else:
				messages.error(request, "Błędny login lub hasło")
		else:
			messages.error(request, "Błędny login lub hasło")

	form = AuthenticationForm()
	return render(request, "blog/login.html", {'form':form})


def logout_request(request):
	logout(request)
	messages.info(request, "Wylogowano!")
	return redirect('blog-home')


def add_meeting(request):
	context = {
		'cities': City.objects.all().order_by('name'),
		'employee': User.objects.all().exclude(id = request.user.id).order_by('first_name'),
	}	
	return render(request, 'blog/add_meetings.html', context)


def add_phonecall(request):
	pass


def client_detail(request, id=None):
	if id:
		client = get_object_or_404(Company, id=id)
		phonecalls = PhoneCalls.objects.filter(company_id=id)
		meetings = Meeting.objects.filter(company_id=id)
		context = {
			"name": client.name,
			"city": client.city,
			"phonecalls": phonecalls,
			"meetings": meetings,
		}

		return render(request, "blog/client.html", context)

	else:
		context = {
		"name": "no context",
		"city": 1,
		}
		return render(request, "blog/client.html", context)


