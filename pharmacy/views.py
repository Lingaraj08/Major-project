import email
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from hospital.models import Patient, User
from pharmacy.models import Medicine, Cart, Order, Pharmacist
from .utils import searchMedicines
from django.views.decorators.csrf import csrf_exempt


# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver


# Create your views here.

# function to return views for the urls

@csrf_exempt
@login_required(login_url="login")
def pharmacy_single_product(request,pk):
     if request.user.is_authenticated and request.user.is_patient:
         
        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.get(serial_number=pk)
        orders = Order.objects.filter(user=request.user, ordered=False)
        carts = Cart.objects.filter(user=request.user, purchased=False)
        if carts.exists() and orders.exists():
            order = orders[0]
            context = {'patient': patient, 'medicines': medicines,'carts': carts,'order': order, 'orders': orders}
            return render(request, 'pharmacy/product-single.html',context)
        else:
            context = {'patient': patient, 'medicines': medicines,'carts': carts,'orders': orders}
            return render(request, 'pharmacy/product-single.html',context)
     else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')  

@csrf_exempt
@login_required(login_url="login")
def pharmacy_shop(request):
    if request.user.is_authenticated and request.user.is_patient:
        
        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()
        orders = Order.objects.filter(user=request.user, ordered=False)
        carts = Cart.objects.filter(user=request.user, purchased=False)
        
        medicines, search_query = searchMedicines(request)
        
        if carts.exists() and orders.exists():
            order = orders[0]
            context = {'patient': patient, 'medicines': medicines,'carts': carts,'order': order, 'orders': orders, 'search_query': search_query}
            return render(request, 'Pharmacy/shop.html', context)
        else:
            context = {'patient': patient, 'medicines': medicines,'carts': carts,'orders': orders, 'search_query': search_query}
            return render(request, 'Pharmacy/shop.html', context)
    
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')  

@csrf_exempt
@login_required(login_url="login")
def checkout(request):
    return render(request, 'pharmacy/checkout.html')

@csrf_exempt
@login_required(login_url="login")
def add_to_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:
         
        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()
        
        item = get_object_or_404(Medicine, pk=pk)
        order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item[0].quantity += 1
                order_item[0].save()
                # messages.warning(request, "This item quantity was updated!")
                context = {'patient': patient,'medicines': medicines, 'order': order}
                return render(request, 'pharmacy/shop.html', context)
            
            else:
                order.orderitems.add(order_item[0])
                # messages.warning(request, "This item is added to your cart!")
                context = {'patient': patient,'medicines': medicines,'order': order}
                return render(request, 'pharmacy/shop.html', context)
        else:
            order = Order(user=request.user)
            order.save()
            order.orderitems.add(order_item[0])
            # messages.warning(request, "This item is added to your cart!")
            context = {'patient': patient,'medicines': medicines,'order': order}
            return render(request, 'pharmacy/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')  

@csrf_exempt
@login_required(login_url="login")
def cart_view(request):
    if request.user.is_authenticated and request.user.is_patient:
         
        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()
        
        carts = Cart.objects.filter(user=request.user, purchased=False)
        orders = Order.objects.filter(user=request.user, ordered=False)
        if carts.exists() and orders.exists():
            order = orders[0]
            context = {'carts': carts,'order': order}
            return render(request, 'Pharmacy/cart.html', context)
        else:
            messages.warning(request, "You don't have any item in your cart!")
            context = {'patient': patient,'medicines': medicines}
            return render(request, 'pharmacy/shop.html', context)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'patient-login.html') 

@csrf_exempt
@login_required(login_url="login")
def remove_from_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:
         
        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()
        carts = Cart.objects.filter(user=request.user, purchased=False)
        
        item = get_object_or_404(Medicine, pk=pk)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, "This item was remove from your cart!")
                context = {'carts': carts,'order': order}
                return render(request, 'Pharmacy/cart.html', context)
            else:
                messages.info(request, "This item was not in your cart")
                context = {'patient': patient,'medicines': medicines}
                return render(request, 'pharmacy/shop.html', context)
        else:
            messages.info(request, "You don't have an active order")
            context = {'patient': patient,'medicines': medicines}
            return render(request, 'pharmacy/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html') 


@csrf_exempt
@login_required(login_url="login")
def increase_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:
         
        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()
        carts = Cart.objects.filter(user=request.user, purchased=False)
        item = get_object_or_404(Medicine, pk=pk)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                if order_item.quantity >= 1:
                    order_item.quantity += 1
                    order_item.save()
                    messages.warning(request, f"{item.name} quantity has been updated")
                    context = {'carts': carts,'order': order}
                    return render(request, 'Pharmacy/cart.html', context)
            else:
                messages.warning(request, f"{item.name} is not in your cart")
                context = {'patient': patient,'medicines': medicines}
                return render(request, 'pharmacy/shop.html', context)
        else:
            messages.warning(request, "You don't have an active order")
            context = {'patient': patient,'medicines': medicines}
            return render(request, 'pharmacy/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html') 


@csrf_exempt
@login_required(login_url="login")
def decrease_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:
         
        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()
        carts = Cart.objects.filter(user=request.user, purchased=False)
        item = get_object_or_404(Medicine, pk=pk)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.warning(request, f"{item.name} quantity has been updated")
                    context = {'carts': carts,'order': order}
                    return render(request, 'Pharmacy/cart.html', context)
                else:
                    order.orderitems.remove(order_item)
                    order_item.delete()
                    messages.warning(request, f"{item.name} item has been removed from your cart")
                    context = {'carts': carts,'order': order}
                    return render(request, 'Pharmacy/cart.html', context)
            else:
                messages.info(request, f"{item.name} is not in your cart")
                context = {'patient': patient,'medicines': medicines}
                return render(request, 'pharmacy/shop.html', context)
        else:
            messages.info(request, "You don't have an active order")
            context = {'patient': patient,'medicines': medicines}
            return render(request, 'pharmacy/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html') 


# Pharmacist Login View
@csrf_exempt
def pharmacist_login(request):
    if request.method == 'GET':
        return render(request, 'pharmacist-login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
                
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            if request.user.is_pharmacist:
                messages.success(request, 'Welcome Pharmacist!')
                return redirect('pharmacist-dashboard')
            else:
                messages.error(request, 'Invalid credentials. Not a Pharmacist')
                return redirect('pharmacist-logout')   
        else:
            messages.error(request, 'Invalid username or password')
            
    return render(request, 'pharmacist-login.html')


# Pharmacist Logout View
@csrf_exempt
def pharmacist_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return render(request, 'pharmacist-login.html')


# Pharmacist Dashboard - Medicines List
@csrf_exempt
@login_required(login_url="pharmacist-login")
def pharmacist_dashboard(request):
    if request.user.is_authenticated and request.user.is_pharmacist:
        try:
            pharmacist = Pharmacist.objects.get(user=request.user)
        except:
            pharmacist = None
        
        medicines = Medicine.objects.all()
        context = {'pharmacist': pharmacist, 'medicines': medicines}
        return render(request, 'pharmacist-dashboard.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return redirect('pharmacist-login')


# Medicines List View
@csrf_exempt
@login_required(login_url="pharmacist-login")
def medicines_list(request):
    if request.user.is_authenticated and request.user.is_pharmacist:
        try:
            pharmacist = Pharmacist.objects.get(user=request.user)
        except:
            pharmacist = None
        
        medicines = Medicine.objects.all()
        context = {'pharmacist': pharmacist, 'medicines': medicines}
        return render(request, 'medicines-list.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return redirect('pharmacist-login')


# Add Medicine View
@csrf_exempt
@login_required(login_url="pharmacist-login")
def add_medicine(request):
    if request.user.is_authenticated and request.user.is_pharmacist:
        from .forms import MedicineForm
        
        if request.method == 'POST':
            form = MedicineForm(request.POST, request.FILES)
            if form.is_valid():
                medicine = form.save(commit=False)
                # Generate medicine ID if not provided
                if not medicine.medicine_id:
                    import random
                    import string
                    medicine.medicine_id = 'MED-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                medicine.save()
                messages.success(request, f'Medicine "{medicine.name}" added successfully!')
                return redirect('pharmacist-dashboard')
            else:
                messages.error(request, 'Error adding medicine. Please check the form.')
        else:
            form = MedicineForm()
        
        try:
            pharmacist = Pharmacist.objects.get(user=request.user)
        except:
            pharmacist = None
        
        context = {'form': form, 'pharmacist': pharmacist}
        return render(request, 'add-medicine.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return redirect('pharmacist-login')


# Edit Medicine View
@csrf_exempt
@login_required(login_url="pharmacist-login")
def edit_medicine(request, pk):
    if request.user.is_authenticated and request.user.is_pharmacist:
        from .forms import MedicineForm
        
        medicine = get_object_or_404(Medicine, serial_number=pk)
        
        if request.method == 'POST':
            form = MedicineForm(request.POST, request.FILES, instance=medicine)
            if form.is_valid():
                form.save()
                messages.success(request, f'Medicine "{medicine.name}" updated successfully!')
                return redirect('pharmacist-dashboard')
            else:
                messages.error(request, 'Error updating medicine. Please check the form.')
        else:
            form = MedicineForm(instance=medicine)
        
        try:
            pharmacist = Pharmacist.objects.get(user=request.user)
        except:
            pharmacist = None
        
        context = {'form': form, 'pharmacist': pharmacist, 'medicine': medicine}
        return render(request, 'edit-medicine.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return redirect('pharmacist-login')


# Delete Medicine View
@csrf_exempt
@login_required(login_url="pharmacist-login")
def delete_medicine(request, pk):
    if request.user.is_authenticated and request.user.is_pharmacist:
        medicine = get_object_or_404(Medicine, serial_number=pk)
        medicine_name = medicine.name
        medicine.delete()
        messages.success(request, f'Medicine "{medicine_name}" deleted successfully!')
        return redirect('pharmacist-dashboard')
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return redirect('pharmacist-login')
