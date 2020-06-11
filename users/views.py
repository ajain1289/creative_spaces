from django.shortcuts import render, HttpResponse, redirect
from backend_app.forms import RoleDetailForm
from users.models import Questionnaire
from users.forms import QuestionnaireForm, ReviewsForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from backend_app.models import UserRole, RoleDetails
from professionals.models import Projects
from django.contrib.auth.hashers import make_password
from misc_files.generic_functions import generate_string
from misc_files.mailing import send_verify_link
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.views import login_required
from backend_app.views import decorators


@method_decorator(csrf_exempt, name='dispatch')
class UserRegistration(View):
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
            f.role_id = UserRole.objects.get(role_name='user').role_id
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


@login_required
def user_index(request):
    return render(request, 'admin_index.html')


def ask_a_question(request):
    prof = RoleDetails.objects.filter(role_id=UserRole.objects.get(role_name='professional').role_id)
    return render(request, 'ask_a_question.html', {'professionals': prof})


@csrf_exempt
def question(request):
    p_email = RoleDetails.objects.get(pk=request.GET['id']).email
    if request.method == 'POST':
        if RoleDetails.objects.filter(email=request.POST['u_email']).exists() and RoleDetails.objects.get(
                email=request.POST['u_email']).role_id == UserRole.objects.get(role_name='user').role_id:
            form = QuestionnaireForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.p_email = p_email
                f.u_email = request.POST['u_email']
                f.question = request.POST['question']
                f.save()
                return redirect('/')
        return render(request, 'question.html', {'invalid_email': True, 'p_email': p_email})
    return render(request, 'question.html', {'p_email':p_email})


@csrf_exempt
@login_required
def answer_questions(request):
    ques = Questionnaire.objects.filter(u_email=request.user.email, status=1)
    return render(request, 'answers.html', {'questions': ques})


@csrf_exempt
@login_required
def add_review(request):
    p_email = Projects.objects.get(pk=request.GET['id']).email
    if request.method == 'POST':
        form = ReviewsForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.p_email = p_email
            f.u_email = request.user.email
            f.rating = request.POST['rating']
            f.review = request.POST['review']
            f.save()
            return redirect('/')
    return render(request, 'add_review.html')


@login_required
def view_profile(request):
    detail = RoleDetails.objects.get(pk=request.GET['id'])
    return render(request, 'view_professional_detail.html', {'detail': detail})