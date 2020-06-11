from django.shortcuts import render, redirect, HttpResponse, Http404
from backend_app.models import RoleDetails, UserRole, Categories, ProductDetails, TemporaryCart, Sales, InvoiceTable
from professionals.models import Projects
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from misc_files.mailing import send_verify_link
from misc_files.generic_functions import generate_string
from django.views import View
from backend_app.forms import RoleDetailForm, CategoriesForm, ProductDetailForm, TemporaryCartForm, SalesForm, InvoiceTableForm
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import login_required
from django.db.models import Sum
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.conf import settings


@method_decorator(csrf_exempt, name='dispatch')
class AdminRegistration(View):
    form = RoleDetailForm()

    def get(self, request):
        return render(request, 'registration.html')

    def post(self, request):
        self.form = RoleDetailForm(request.POST)
        if self.form.is_valid():
            if request.FILES:
                filename = request.FILES['image']
                fs = FileSystemStorage()
                my_file = fs.save(filename.name, filename)
                image = fs.url(my_file)
                image = filename.name
            f = self.form.save(commit=False)
            f.role_id = UserRole.objects.get(role_name='admin').role_id
            f.first_name = request.POST['first_name']
            f.last_name = request.POST['last_name']
            f.username = request.POST['first_name'] + "_" + request.POST['last_name']
            f.email = request.POST['email']
            f.image = image
            f.mobile = request.POST['mobile']
            f.password = make_password(request.POST['password'])
            f.address = request.POST['address']
            token = make_password(generate_string()).replace("+", "")
            verify_link = '127.0.0.1:8000/verify/?token={}'.format(token)
            f.verify_link = token
            f.is_staff = False
            f.is_superuser = False
            f.is_active = False
            f.save()
            try:
                send_verify_link(request.POST['email'], f.username, verify_link)
            except:
                print("!!!!!  Failed to send email  !!!!!")
            return redirect('/')
        else:
            return HttpResponse(status=400)


decorators = [login_required, csrf_exempt]


@method_decorator(decorators, name='dispatch')
class AddProduct(View):
    form = ProductDetailForm()

    def get(self, request):
        categories = Categories.objects.all()
        return render(request, 'add_product.html', {'categories': categories})

    def post(self, request):
        self.form = ProductDetailForm(request.POST)
        if self.form.is_valid():
            if request.FILES:
                filename1 = request.FILES['cover_photo']
                filename2 = request.FILES['photo']
                fs = FileSystemStorage()
                my_file1 = fs.save(filename1.name, filename1)
                my_file2 = fs.save(filename2.name, filename2)
                image1 = fs.url(my_file1)
                image2 = fs.url(my_file2)
                cover_photo = filename1.name
                photo = filename2.name
            f = self.form.save(commit=False)
            f.category_id = request.POST['cat']
            f.p_name = request.POST['p_name']
            f.price = request.POST['price']
            f.quantity = request.POST['quantity']
            f.description = request.POST['description']
            f.cover_photo = cover_photo
            f.photo = photo
            f.save()
        else:
            return HttpResponse(status=400)
        return redirect('/admin_index/')


def index(request):
    data = RoleDetails.objects.filter(role_id=UserRole.objects.get(role_name='admin').role_id).exists()
    categories = Categories.objects.all()
    products = ProductDetails.objects.all()
    professionals = RoleDetails.objects.filter(role__role_name='professional')[:3]
    products_dict = dict()
    for product in products:
        if product.category_id not in products_dict:
            products_dict.update({product.category_id: product})
    if data is True:
        request.session['admin_exists'] = True
    return render(request, 'index.html', {'categories': categories, 'products': products_dict.values(), 'professionals': professionals})


def about_us(request):
    return render(request, 'about_us.html')


def portfolio(request):
    projects = Projects.objects.all()
    return render(request, 'portfolio.html', {'projects': projects})


@method_decorator(csrf_exempt, name='dispatch')
class MyLogin(View):
    def get(self, request, message=None):
        if message is None:
            if request.session.get('_auth_user_id') is None:
                return render(request, 'login.html')
            else:
                role = RoleDetails.objects.get(pk=request.session.get('_auth_user_id')).role.role_name
                if role == 'admin':
                    return redirect('/admin_index/')
                elif role == 'professional':
                    return redirect('/professional/index/')
                elif role == 'user':
                    return redirect('/user/index/')
        else:
            return render(request, 'login.html', {message: True})

    def post(self, request):
        try:
            detail = RoleDetails.objects.get(email=request.POST['email'])
        except:
            return self.get(request, 'email_invalid')
        else:
            if check_password(request.POST['password'], detail.password):
                if detail.is_active is True:
                    user = authenticate(request, username=detail.username, password=request.POST['password'])
                    if user is not None:
                        login(request, user)
                        request.session['image'] = detail.image
                        request.session['role'] = detail.role.role_name
                        request.session['logged_in'] = True
                        if detail.role.role_name == 'admin':
                            return redirect('/admin_index/')
                        elif detail.role.role_name == 'user':
                            return redirect('/user/index/')
                        elif detail.role.role_name == 'professional':
                            return redirect('/professional/index/')
                else:
                    return self.get(request, 'not_verify')
            else:
                return self.get(request, 'password_invalid')


@method_decorator(decorators, name='dispatch')
class UpdatePassword(View):
    def get(self, request, message=None):
        if message is None:
            return render(request, 'update_password.html')
        else:
            return render(request, 'update_password.html', {message: True})

    def post(self, request):
        detail = RoleDetails.objects.get(pk=request.session.get('_auth_user_id'))
        if check_password(request.POST['old_password'], detail.password):
            if request.POST['new_password'] == request.POST['confirm_password']:
                password = make_password(request.POST['new_password'])
                update = RoleDetails(id=detail.id, password=password)
                update.save(update_fields=['password'])

                role = RoleDetails.objects.get(pk=request.session.get('_auth_user_id')).role.role_name
                if role == 'admin':
                    return redirect('/admin_index/')
                elif role == 'professional':
                    return redirect('/professional/index/')
                elif role == 'user':
                    return redirect('/user/index/')
            else:
                return self.get(request, 'passwords_donot_match')
        else:
            return self.get(request, 'invalid_password')


@csrf_exempt
@login_required
def add_category(request):
    if request.method == "POST":
        image = request.session['image']
        form = CategoriesForm(request.POST)
        if form.is_valid():
            if request.FILES:
                filename = request.FILES['image']
                fs = FileSystemStorage()
                my_file = fs.save(filename.name, filename)
                image = fs.url(my_file)
                image = filename.name
            f = form.save(commit=False)
            f.c_name = request.POST['category_add']
            f.image = image
            f.save()
            return redirect('/view_categories/')
    return render(request, 'add_category.html')


@login_required
def admin_index(request):
    return render(request, 'admin_index.html')


@login_required
def view_categories(request):
    category = Categories.objects.all()
    return render(request, 'view_categories.html', {'categories': category})


@csrf_exempt
@login_required
def update_category(request, pk):
    data = Categories.objects.get(pk=pk)
    if request.method == 'POST':
        image = data.image
        if request.FILES:
            filename = request.FILES['image']
            fs = FileSystemStorage()
            my_file = fs.save(filename.name, filename)
            image = fs.url(my_file)
            image = filename.name
        name = request.POST['cattt']
        update = Categories(c_id=data.c_id, c_name=name, image=image)
        update.save(update_fields=['c_name', 'image'])
        return redirect('/view_categories/')
    return render(request, 'update_category.html', {'data': data})


@login_required
def my_logout(request):
    logout(request)
    request.session.flush()
    return redirect('/')


@method_decorator(csrf_exempt, name='dispatch')
class ChangePassword(View):
    def get(self, request):
        return render(request, 'change_password.html')

    def post(self, request):
        detail = RoleDetails.objects.get(email=request.session['email'])
        password = make_password(request.POST['password'])
        update = RoleDetails(id=detail.id, password=password)
        update.save(update_fields=['password'])
        request.session.pop('email')
        return redirect('/login/')


@method_decorator(csrf_exempt, name='dispatch')
class ForgotPassword(View):
    def get(self, request, message=None):
        if message is None:
            return render(request, 'forgot_password.html')
        else:
            return render(request, 'forgot_password.html', {message: True})

    def post(self, request):
        try:
            detail = RoleDetails.objects.get(email=request.POST['email'])
        except:
            return self.get(request, 'email_not_registered')
        else:
            token = make_password(request.POST['email']).replace("+","")
            verify_link = '127.0.0.1:8000/forgot_password_verify/?token={}'.format(token)
            try:
                send_verify_link(request.POST['email'], 'User', verify_link)
                request.session['email'] = detail.email
            except:
                print("!!!!!  Failed to send email  !!!!!")
            return redirect('/')


def user_verification(request):
    try:
        token = request.GET['token']
    except:
        return Http404
    else:
        try:
            RoleDetails.objects.get(verify_link=token)
        except:
            return Http404
        else:
            RoleDetails(pk=RoleDetails.objects.get(verify_link=token).pk, is_active=True, verify_link='').save(
                update_fields=['is_active', 'verify_link'])
            return redirect('/login/')


def forgot_password_verification(request):
    try:
        token = request.GET['token']
    except:
        return Http404
    else:
        try:
            mail_id = request.session['email']
        except:
            return Http404
        else:
            if check_password(mail_id, token):
                return redirect('/change_password/')
            else:
                return Http404


@login_required
def view_products(request):
    products = ProductDetails.objects.all()
    categories = Categories.objects.all()
    try:
        category = request.GET['category']
    except:
        return render(request, 'view_products.html', {'products': products, 'categories': categories})
    else:
        product_filter = ProductDetails.objects.filter(category_id=category)
        return render(request, 'view_products.html', {'products': product_filter, 'categories': categories})


@csrf_exempt
@login_required
def update_product(request, pk):
    data = ProductDetails.objects.get(pk=pk)
    if request.method == 'POST':
        if not len(request.FILES) == 0:
            if request.FILES:
                for i in request.FILES:
                    filename = request.FILES[i]
                    fs = FileSystemStorage()
                    my_file = fs.save(filename.name, filename)
                    image = fs.url(my_file)
                    image = filename.name
                    if i == 'cover_photo':
                        update = ProductDetails(pk=data.pk, cover_photo=image)
                        update.save(update_fields=['cover_photo'])
                    elif i == 'photo':
                        update = ProductDetails(pk=data.pk, photo=image)
                        update.save(update_fields=['photo'])
        p_name = request.POST['p_name']
        price = request.POST['price']
        description = request.POST['description']
        quantity = request.POST['quantity']
        update = ProductDetails(p_id=data.p_id, p_name=p_name, price=price, description=description, quantity=quantity)
        update.save(update_fields=['p_name', 'price', 'description', 'quantity'])
        return redirect('/view_products/')
    return render(request, 'update_product.html', {'data': data})


@csrf_exempt
@login_required
def update_my_profile(request):
    detail = RoleDetails.objects.get(pk=request.session.get('_auth_user_id'))
    if request.method == 'POST':
        image = detail.image
        if request.FILES:
            filename = request.FILES['photo']
            fs = FileSystemStorage()
            my_file = fs.save(filename.name, filename)
            image = fs.url(my_file)
            image = filename.name
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        mobile = request.POST['mobile']
        image_update = image
        request.session['image'] = image_update
        update = RoleDetails(id=detail.id, first_name=first_name, last_name=last_name, address=address, mobile=mobile,
                             image=image_update)
        update.save(update_fields=['first_name', 'last_name', 'address', 'mobile', 'image'])
        return redirect('/admin_index/')
    return render(request, 'update_my_profile.html', {'detail': detail})


def products(request):
    product = ProductDetails.objects.all()
    cat = Categories.objects.all()
    pid_list = TemporaryCart.objects.values_list('product')
    temp_data = []
    for i in pid_list:
        for j in i:
            temp_data.append(j)
    try:
        category = request.GET['category']
    except:
        return render(request, 'products.html', {'products': product, 'categories': cat, 'temp_data': temp_data})
    else:
        product_filter = ProductDetails.objects.filter(category_id=category)
        return render(request, 'products.html', {'categories': cat, 'products': product_filter, 'temp_data': temp_data})


def add_to_cart(request, pk):
    if not TemporaryCart.objects.filter(product=pk).exists():
        form = TemporaryCartForm(request.POST)
        detail = ProductDetails.objects.get(pk=pk)
        if form.is_valid():
            f = form.save(commit=False)
            f.product = detail.pk
            f.p_name = detail.p_name
            f.quantity = 1
            f.price = detail.price
            f.total_price = f.quantity * f.price
            f.image = detail.cover_photo
            f.save()
            data = ProductDetails.objects.get(p_id=detail.pk)
            temp_data = TemporaryCart.objects.get(product=pk)
            return render(request, 'view_product_detail.html', {'data': data, 'temp_data': temp_data})
    else:
        if TemporaryCart.objects.filter(product=pk).exists():
            data = ProductDetails.objects.get(p_id=pk)
            temp_data = TemporaryCart.objects.get(product=pk)
            return render(request, 'view_product_detail.html', {'data': data, 'temp_data': temp_data})
        else:
            return redirect('/products/')


def show_cart(request):
    data = TemporaryCart.objects.all()
    return render(request, 'show_cart.html', {'data': data})


def delete_cart_item(request, pk):
    if TemporaryCart.objects.filter(pk=pk).exists():
        data = TemporaryCart.objects.get(pk=pk)
        data.delete()
        return redirect('/show_cart/')
    else:
        return redirect('/show_cart/')


def qty_increase_decrease(request):
    t_id = request.GET.get('t_id')
    qty = request.GET.get('qty')
    update = TemporaryCart(t_id=t_id, quantity=qty, total_price=int(TemporaryCart.objects.get(pk=t_id).price) * int(qty))
    update.save(update_fields=['quantity', 'total_price'])


address_dict = dict()


@csrf_exempt
@login_required
def checkout_page(request):
    global address_dict
    data = RoleDetails.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        address_dict.update({
            'name': request.POST['name'],
            'email': request.POST['email'],
            'address': request.POST['address'],
            'mobile': request.POST['mobile']
        })
        return redirect('/payment_processing/')
    return render(request, 'checkout_page.html', {'data': data})


@login_required
def payment_processing(request):
    global address_dict
    form = InvoiceTableForm(request.GET)
    token = generate_string(5)
    if form.is_valid():
        f = form.save(commit=False)
        f.u_email = request.user.email
        f.token = token
        f.save()
    invoice_no = InvoiceTable.objects.get(u_email=request.user.email, token=token).invoice
    token = make_password(token).replace("+", "")
    request.session['token'] = token
    request.session['invoice'] = invoice_no
    host = request.get_host()
    total = TemporaryCart.objects.all().aggregate(Sum('total_price'))
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total['total_price__sum']/75.59,
        'item_name': 'Home Decor',
        'invoice': invoice_no,
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}?token={}'.format(host, reverse('payment_successful'), request.session['token'])
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment_processing.html', {'form': form, 'total': total['total_price__sum'], 'address_dict': address_dict})


@login_required
def payment_successful(request):
    invoice = request.session['invoice']
    token = request.GET['token']
    if request.session['token'] == token:
        data = TemporaryCart.objects.all()
        total = TemporaryCart.objects.all().aggregate(Sum('total_price'))
        for i in data:
            form = SalesForm(request.GET)
            if form.is_valid():
                f = form.save(commit=False)
                f.product = i.product
                f.p_name = i.p_name
                f.price = i.price
                f.quantity = i.quantity
                f.total_price = i.total_price
                f.image = i.image
                f.u_email = request.user.email
                f.save()
                qty = ProductDetails.objects.get(pk=f.product).quantity
                update = ProductDetails(pk=f.product, quantity=int(qty)-int(f.quantity))
                update.save(update_fields=['quantity'])
        data.delete()
        update = InvoiceTable(request.session['invoice'], status=1, amount=total['total_price__sum'])
        update.save(update_fields=['status', 'amount'])
        return render(request, 'payment_successful.html', {'invoice': invoice})


@login_required
def payment_failed(request):
    return render(request, 'payment_failed.html')


@login_required
def delete_category(request, pk):
    if Categories.objects.filter(pk=pk).exists():
        data = Categories.objects.get(pk=pk)
        data.delete()
        return redirect('/view_categories/')
    else:
        return redirect('/view_categories/')


@login_required
def delete_product(request, pk):
    if ProductDetails.objects.filter(pk=pk).exists():
        data = ProductDetails.objects.get(pk=pk)
        data.delete()
        return redirect('/view_products/')
    else:
        return redirect('/view_products/')