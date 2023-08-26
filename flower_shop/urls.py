"""
URL configuration for flower_shop project.
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from flower_shop_site import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.show_catalog, name='catalog'),
    path('quiz-step/', views.quiz_step, name='quiz-step'),
    path('quiz/', views.quiz, name='quiz'),
    path('result/', views.show_quiz_result, name='result'),
    path('order/', views.make_order, name='make_order'),
    path('accept_payment/', views.accept_payment, name='accept_payment'),
    path('order-step/', views.make_order_step, name='make_order_step'),
    path('consultation/', views.order_consultation, name='consultation'),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
