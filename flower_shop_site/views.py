from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Bouquet


def index(request):
    bouquets = Bouquet.objects.order_by('?')[:3]
    context = {
        'is_index_page': True,
        'bouquets': bouquets
    }
    return render(request, 'index.html', context)


def show_catalog(request):
    bouquet_list = Bouquet.objects.all()
    paginator = Paginator(bouquet_list, 6)

    page = request.GET.get('page')
    try:
        bouquets = paginator.page(page)
    except PageNotAnInteger:
        bouquets = paginator.page(1)
    except EmptyPage:
        bouquets = paginator.page(paginator.num_pages)

    return render(request, 'catalog.html', context={'bouquets': bouquets})


def quiz_step(request):
    return render(request, 'quiz-step.html')


def quiz(request):
    return render(request, 'quiz.html')


def show_quiz_result(request):
    return render(request, 'result.html')


def make_order(request):
    return render(request, 'order.html')


def order_consultation(request):
    return render(request, 'consultation.html')
