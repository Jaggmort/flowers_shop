import os
import dotenv
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Bouquet, Consultation, Order
from .notifications_bot import unify_phone
from yookassa import Configuration, Payment


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


def accept_payment(request):
    order = Order.objects.last()
    order.is_payed = True
    order.save()
    return render(request, 'index.html')


def accept_payment1(request):
    with open('test.txt', 'w') as file:
        file.write('whatever')
    return render(request, 'index.html')


def make_order_step(request):
    dotenv.load_dotenv('.env')
    Configuration.account_id = os.environ['SHOP_ACCOUNT_ID']
    Configuration.secret_key = os.environ['SHOP_SECRET_KEY']
    if request.GET:
        fname = request.GET.get('fname')
        tel = request.GET.get('tel')
        adres = request.GET.get('adres')
        time = request.GET.get('orderTime')
        bouquet = Bouquet.objects.first()
        order = Order.objects.create(
            bouquet=bouquet,
            client_name=fname,
            phone_number=tel,
            delivery_time=time,
            address=adres
            )
        payment = Payment.create({
            "amount": {
                "value": "100.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://www.jaggmort.ru/accept_payment",
            },
            "capture": True,
            "description": "Заказ №37",
            "metadata": {
                "order_id": order.id
            }
        })
        return redirect(payment.confirmation.confirmation_url)
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
