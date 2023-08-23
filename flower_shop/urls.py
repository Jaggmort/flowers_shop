"""
URL configuration for flower_shop project.
"""
from django.contrib import admin
from django.urls import path, include
from flower_shop_site import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.show_catalog, name='catalog'),
    path('quiz-step/', views.quiz_step, name='quiz-step'),
    path('quiz/', views.quiz, name='quiz'),
    path('result/', views.show_quiz_result, name='result'),
    path('order/', views.make_order, name='make_order'),
    path('consultation/', views.order_consultation, name='consultation'),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
]
