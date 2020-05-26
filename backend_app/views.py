from django.shortcuts import render, redirect, HttpResponse, Http404
from backend_app.models import RoleDetails, UserRole
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from misc_files.mailing import send_verify_link
from misc_files.generic_functions import generate_string
from django.views import View
from backend_app.forms import RoleDetailForm
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import login_required


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


def index(request):
    data = RoleDetails.objects.filter(role_id=UserRole.objects.get(role_name='admin').role_id).exists()
    if data is True:
        request.session['admin_exists'] = True
    return render(request, 'index.html')


def about_us(request):
    return render(request, 'about_us.html')


def contact_us(request):
    return render(request, 'contact_us.html')


def gallery(request):
    return render(request, 'gallery.html')


def profile(request):
    return render(request, 'profile.html')


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
            RoleDetails(pk=RoleDetails.objects.get(verify_link=token).pk, is_active=True, verify_link='').save(update_fields=['is_active', 'verify_link'])
            return redirect('/login/')


@login_required
def admin_index(request):
    return render(request, 'admin_index.html')


@login_required
def my_logout(request):
    logout(request)
    request.session.flush()
    return redirect('/')
