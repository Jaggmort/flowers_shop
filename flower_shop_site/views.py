from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'index.html', context)


def show_catalog(request):
    context = {}
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
    return render(request, 'consultation.html')
