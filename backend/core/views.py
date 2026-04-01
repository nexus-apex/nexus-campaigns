import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Campaign, Subscriber, EmailTemplate


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['campaign_count'] = Campaign.objects.count()
    ctx['campaign_newsletter'] = Campaign.objects.filter(campaign_type='newsletter').count()
    ctx['campaign_promotional'] = Campaign.objects.filter(campaign_type='promotional').count()
    ctx['campaign_drip'] = Campaign.objects.filter(campaign_type='drip').count()
    ctx['campaign_total_open_rate'] = Campaign.objects.aggregate(t=Sum('open_rate'))['t'] or 0
    ctx['subscriber_count'] = Subscriber.objects.count()
    ctx['subscriber_active'] = Subscriber.objects.filter(status='active').count()
    ctx['subscriber_unsubscribed'] = Subscriber.objects.filter(status='unsubscribed').count()
    ctx['subscriber_bounced'] = Subscriber.objects.filter(status='bounced').count()
    ctx['emailtemplate_count'] = EmailTemplate.objects.count()
    ctx['emailtemplate_welcome'] = EmailTemplate.objects.filter(category='welcome').count()
    ctx['emailtemplate_promo'] = EmailTemplate.objects.filter(category='promo').count()
    ctx['emailtemplate_newsletter'] = EmailTemplate.objects.filter(category='newsletter').count()
    ctx['recent'] = Campaign.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def campaign_list(request):
    qs = Campaign.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(campaign_type=status_filter)
    return render(request, 'campaign_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def campaign_create(request):
    if request.method == 'POST':
        obj = Campaign()
        obj.name = request.POST.get('name', '')
        obj.campaign_type = request.POST.get('campaign_type', '')
        obj.status = request.POST.get('status', '')
        obj.sent_count = request.POST.get('sent_count') or 0
        obj.open_rate = request.POST.get('open_rate') or 0
        obj.click_rate = request.POST.get('click_rate') or 0
        obj.scheduled_date = request.POST.get('scheduled_date') or None
        obj.save()
        return redirect('/campaigns/')
    return render(request, 'campaign_form.html', {'editing': False})


@login_required
def campaign_edit(request, pk):
    obj = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.campaign_type = request.POST.get('campaign_type', '')
        obj.status = request.POST.get('status', '')
        obj.sent_count = request.POST.get('sent_count') or 0
        obj.open_rate = request.POST.get('open_rate') or 0
        obj.click_rate = request.POST.get('click_rate') or 0
        obj.scheduled_date = request.POST.get('scheduled_date') or None
        obj.save()
        return redirect('/campaigns/')
    return render(request, 'campaign_form.html', {'record': obj, 'editing': True})


@login_required
def campaign_delete(request, pk):
    obj = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/campaigns/')


@login_required
def subscriber_list(request):
    qs = Subscriber.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(email__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'subscriber_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def subscriber_create(request):
    if request.method == 'POST':
        obj = Subscriber()
        obj.email = request.POST.get('email', '')
        obj.name = request.POST.get('name', '')
        obj.status = request.POST.get('status', '')
        obj.list_name = request.POST.get('list_name', '')
        obj.subscribed_date = request.POST.get('subscribed_date') or None
        obj.tags = request.POST.get('tags', '')
        obj.save()
        return redirect('/subscribers/')
    return render(request, 'subscriber_form.html', {'editing': False})


@login_required
def subscriber_edit(request, pk):
    obj = get_object_or_404(Subscriber, pk=pk)
    if request.method == 'POST':
        obj.email = request.POST.get('email', '')
        obj.name = request.POST.get('name', '')
        obj.status = request.POST.get('status', '')
        obj.list_name = request.POST.get('list_name', '')
        obj.subscribed_date = request.POST.get('subscribed_date') or None
        obj.tags = request.POST.get('tags', '')
        obj.save()
        return redirect('/subscribers/')
    return render(request, 'subscriber_form.html', {'record': obj, 'editing': True})


@login_required
def subscriber_delete(request, pk):
    obj = get_object_or_404(Subscriber, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/subscribers/')


@login_required
def emailtemplate_list(request):
    qs = EmailTemplate.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(category=status_filter)
    return render(request, 'emailtemplate_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def emailtemplate_create(request):
    if request.method == 'POST':
        obj = EmailTemplate()
        obj.name = request.POST.get('name', '')
        obj.subject = request.POST.get('subject', '')
        obj.category = request.POST.get('category', '')
        obj.content = request.POST.get('content', '')
        obj.active = request.POST.get('active') == 'on'
        obj.usage_count = request.POST.get('usage_count') or 0
        obj.save()
        return redirect('/emailtemplates/')
    return render(request, 'emailtemplate_form.html', {'editing': False})


@login_required
def emailtemplate_edit(request, pk):
    obj = get_object_or_404(EmailTemplate, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.subject = request.POST.get('subject', '')
        obj.category = request.POST.get('category', '')
        obj.content = request.POST.get('content', '')
        obj.active = request.POST.get('active') == 'on'
        obj.usage_count = request.POST.get('usage_count') or 0
        obj.save()
        return redirect('/emailtemplates/')
    return render(request, 'emailtemplate_form.html', {'record': obj, 'editing': True})


@login_required
def emailtemplate_delete(request, pk):
    obj = get_object_or_404(EmailTemplate, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/emailtemplates/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['campaign_count'] = Campaign.objects.count()
    data['subscriber_count'] = Subscriber.objects.count()
    data['emailtemplate_count'] = EmailTemplate.objects.count()
    return JsonResponse(data)
