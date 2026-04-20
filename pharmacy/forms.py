from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from hospital.models import User
from .models import Pharmacist, Medicine

# Pharmacist Login Form
class PharmacistLoginForm(forms.Form):
    username = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


# Pharmacist Registration Form
class PharmacistUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(PharmacistUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control floating'})


# Pharmacist Profile Form
class PharmacistForm(ModelForm):
    class Meta:
        model = Pharmacist
        fields = ['name', 'email', 'phone_number', 'degree', 'featured_image', 'age']

    def __init__(self, *args, **kwargs):
        super(PharmacistForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


# Medicine Form for adding/editing medicines
class MedicineForm(ModelForm):
    class Meta:
        model = Medicine
        fields = ['medicine_id', 'name', 'weight', 'quantity', 'featured_image', 'description', 
                  'medicine_type', 'medicine_category', 'price', 'stock_quantity', 'Prescription_reqiuired']
        widgets = {
            'medicine_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medicine ID'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medicine Name', 'required': True}),
            'weight': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Weight (e.g., 500mg)'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Medicine Description'}),
            'medicine_type': forms.Select(attrs={'class': 'form-control'}),
            'medicine_category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price (₹)'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock Quantity'}),
            'Prescription_reqiuired': forms.Select(attrs={'class': 'form-control'}),
        }