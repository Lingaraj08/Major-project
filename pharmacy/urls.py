from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

# from . --> same directory
# Views functions and urls must be linked. # of views == # of urls
# App URL file - urls related to hospital


urlpatterns = [
    # Existing pharmacy URLs
    path('product-single/<int:pk>/', views.pharmacy_single_product, name='product-single'),
    path('shop/', views.pharmacy_shop, name='pharmacy_shop'),
    path('cart/', views.cart_view, name='cart'),
    path('remove-item/<int:pk>/', views.remove_from_cart, name='remove-item'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-to-cart/<int:pk>', views.add_to_cart, name='add-to-cart'),
    path('increase-item/<int:pk>/', views.increase_cart, name='increase-item'),
    path('decrease-item/<int:pk>/', views.decrease_cart, name='decrease-item'),
    
    # Pharmacist URLs
    path('pharmacist-login/', views.pharmacist_login, name='pharmacist-login'),
    path('pharmacist-logout/', views.pharmacist_logout, name='pharmacist-logout'),
    path('pharmacist-dashboard/', views.pharmacist_dashboard, name='pharmacist-dashboard'),
    path('medicines-list/', views.medicines_list, name='medicines-list'),
    path('add-medicine/', views.add_medicine, name='add-medicine'),
    path('edit-medicine/<int:pk>/', views.edit_medicine, name='edit-medicine'),
    path('delete-medicine/<int:pk>/', views.delete_medicine, name='delete-medicine'),
]
    


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
