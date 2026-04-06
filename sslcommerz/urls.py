from unicodedata import name
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin


urlpatterns = [
    path('', views.payment_home, name='payment_home'),
    path('razorpay-payment-request/<int:pk>/<int:id>/', views.razorpay_payment_request,name='razorpay-payment-request'),
    path('razorpay-payment-success/', views.razorpay_payment_success,name='razorpay-payment-success'),
    path('razorpay-payment-fail/', views.razorpay_payment_fail, name='razorpay-payment-fail'),
    path('razorpay-payment-cancel/', views.razorpay_payment_cancel, name='razorpay-payment-cancel'),
    path('razorpay-payment-request-medicine/<int:pk>/<int:id>/', views.razorpay_payment_request_medicine,name='razorpay-payment-request-medicine'),
    path('razorpay-payment-request-test/<int:pk>/<int:id>/<int:pk2>/', views.razorpay_payment_request_test,name='razorpay-payment-request-test'),
    path('verify-payment/', views.verify_payment, name='verify-payment'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
