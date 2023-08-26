from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Bouquet, Consultation
from .notifications_bot import unify_phone


def index(request):
    bouquets = Bouquet.objects.order_by('?')[:3]
    context = {
        'is_index_page': True,
        'bouquets': bouquets
    }
    if request.method == 'POST':
        client_name = request.POST['fname']
        phone_number = unify_phone(request.POST['tel'])
        if phone_number:
            Consultation.objects.create(
                client_name=client_name,
                phone_number=phone_number
            )
            context['sign_up'] = 'success'

    return render(request, 'index.html', context)


def show_catalog(request):
    context = {}
    bouquet_list = Bouquet.objects.all()
    paginator = Paginator(bouquet_list, 6)

    page = request.GET.get('page')
    try:
        bouquets = paginator.page(page)
    except PageNotAnInteger:
        bouquets = paginator.page(1)
    except EmptyPage:
        bouquets = paginator.page(paginator.num_pages)
    context['bouquets'] = bouquets

    if request.method == 'POST':
        client_name = request.POST['fname']
        phone_number = unify_phone(request.POST['tel'])
        if phone_number:
            Consultation.objects.create(
                client_name=client_name,
                phone_number=phone_number
            )
            context['sign_up'] = 'success'

    return render(request, 'catalog.html', context)


def quiz_step(request):
    return render(request, 'quiz-step.html')


def quiz(request):
    return render(request, 'quiz.html')


def show_quiz_result(request):
    return render(request, 'result.html')


def make_order(request):
    return render(request, 'order.html')


def order_consultation(request):
    context = {}
    if request.method == 'POST':
        client_name = request.POST['fname']
        phone_number = unify_phone(request.POST['tel'])
        if phone_number:
            Consultation.objects.create(
                client_name=client_name,
                phone_number=phone_number
            )
            context['sign_up'] = 'success'
    return render(request, 'consultation.html', context)
