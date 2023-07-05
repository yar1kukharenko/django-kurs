from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
import users.models
from records.models import *
from records.forms import *
from users.models import User


@login_required(login_url='users/login/')
def index(request):
    user = request.user
    therapist_records_next = None
    client_records_next = None
    if user.user_type == 'TH':
        therapist = Therapist.objects.get(user=request.user)
        therapist_records_next = therapist.get_records
    elif user.user_type == 'CL':
        client = Clients.objects.get(user=request.user)
        client_records_next = client.get_next_records

    context = {
        'tittle': 'Домашний экран',
        'client_records': client_records_next,
        'therapist_records': therapist_records_next,
        'therapists': Therapist.objects.all(),
    }
    return render(request, 'records/index.html', context)


@login_required(login_url='users/login/')
def lastrecords(request):
    user = request.user
    therapist_records_past = None
    client_records_past = None
    if user.user_type == 'TH':
        therapist = Therapist.objects.get(user=request.user)
        therapist_records_past = therapist.get_past_records()
    elif user.user_type == 'CL':
        client = Clients.objects.get(user=request.user)
        client_records_past = client.get_past_records
    context = {
        'tittle': "История консультаций",
        'client_records': client_records_past,
        'therapist_records': therapist_records_past,
        'user': user,
        'therapists': Therapist.objects.all(),
    }
    return render(request, 'records/lastrecords.html', context)


@login_required(login_url='users/login/')
def cancel_record(request, record_id):
    user = request.user
    record = Records.objects.get(id=record_id)
    if user.user_type == 'CL':
        record.client = None
        record.save()
    elif user.user_type == 'TH':
        record.delete()
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='users/login/')
def addrecord(request):
    if request.method == 'POST':
        form = AddRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.therapist = Therapist.objects.get(user=request.user)
            record.save()
            return HttpResponseRedirect(reverse(index))
    else:
        form = AddRecordForm()
    context = {
        'form': form,
        'tittle': 'Добавить запись'
    }
    return render(request, 'records/addrecord.html', context)


@login_required(login_url='users/login/')
def therapists(request):
    therapists = Therapist.objects.all()
    selected_methods = request.GET.getlist('methods')
    selected_feelings = request.GET.getlist('feelings')
    selected_events = request.GET.getlist('events')
    selected_price = request.GET.getlist('price')
    selected_date = request.GET.getlist('date')
    if request.method == 'GET':
        if selected_events:
            therapists = therapists.filter(events__name__in=selected_events).distinct()
        if selected_feelings:
            therapists = therapists.filter(feelings__name__in=selected_feelings).distinct()
        if selected_methods:
            therapists = therapists.filter(methods__name__in=selected_methods).distinct()

    context = {
        'tittle': 'Терапветы',
        'therapists': therapists,
        # 'records': Records.objects.all(),
        'methods': Methods.objects.all(),
        'feelings': Feelings.objects.all(),
        'events': Events.objects.all(),
        'selected_methods': selected_methods,
        'selected_feelings': selected_feelings,
        'selected_events': selected_events,
        'selected_price': selected_price,
        'selected_date': selected_date,
    }

    return render(request, 'records/therapists.html', context)


@login_required(login_url='users/login/')
def therapist_profile(request, therapist_id):
    therapist = get_object_or_404(Therapist, pk=therapist_id)
    records = therapist.get_records()
    context = {
        'records': records,
        'therapist': therapist
    }
    return render(request, 'records/therapist_profile.html', context)


@login_required(login_url='users/login/')
def record_update(request):
    if request.method == 'POST':
        client = Clients.objects.get(user=request.user)
        record_id = request.POST.get('record_id')
        record = Records.objects.get(id=record_id)
        record.client = client
        record.save()
        HttpResponseRedirect(reverse('index'))

    return HttpResponseRedirect(reverse(index))
