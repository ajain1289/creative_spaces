from django import forms
from backend_app.models import RoleDetails, Categories, ProductDetails, TemporaryCart, Sales, InvoiceTable


class RoleDetailForm(forms.ModelForm):
    class Meta:
        model = RoleDetails
        exclude = ['id', 'last_login', 'is_active', 'date_joined', 'first_name', 'last_name', 'username', 'email', 'mobile', 'password',
                   'role', 'address', 'verify_link', 'image', 'otp', 'otp_time', 'is_staff', 'is_superuser']


class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        exclude = ['c_id', 'c_name', 'image']


class ProductDetailForm(forms.ModelForm):
    class Meta:
        model = ProductDetails
        exclude = ['p_id', 'p_name', 'category', 'price', 'description', 'photo', 'cover_photo', 'quantity']


class TemporaryCartForm(forms.ModelForm):
    class Meta:
        model = TemporaryCart
        exclude = ['t_id', 'product', 'p_name', 'price', 'quantity', 'total_price', 'image']


class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        exclude = ['t_id', 'u_email', 'product', 'p_name', 'price', 'quantity', 'total_price', 'image']


class InvoiceTableForm(forms.ModelForm):
    class Meta:
        model = InvoiceTable
        exclude = ['invoice', 'amount', 'u_email', 'status', 'token']