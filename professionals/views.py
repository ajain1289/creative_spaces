from django.shortcuts import render, HttpResponse, redirect
from backend_app.forms import RoleDetailForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from backend_app.models import UserRole, RoleDetails, Categories
from users.models import Questionnaire
from professionals.models import Projects
from professionals.forms import ProjectsForm
from django.contrib.auth.hashers import make_password
from misc_files.generic_functions import generate_string
from misc_files.mailing import send_verify_link
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.views import login_required
from backend_app.views import decorators


@method_decorator(csrf_exempt, name='dispatch')
class ProfessionalRegistration(View):
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
            f.role_id = UserRole.objects.get(role_name='professional').role_id
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
def professional_index(request):
    return render(request, 'admin_index.html')


@method_decorator(decorators, name='dispatch')
class AddProject(View):
    form = ProjectsForm()

    def get(self, request):
        categories = Categories.objects.all()
        return render(request, 'add_project.html', {'categories': categories})

    def post(self, request):
        self.form = ProjectsForm(request.POST)
        if self.form.is_valid():
            if request.FILES:
                filename1 = request.FILES['photo']
                fs = FileSystemStorage()
                my_file1 = fs.save(filename1.name, filename1)
                image1 = fs.url(my_file1)
                photo = filename1.name
            f = self.form.save(commit=False)
            f.category_id = request.POST['category']
            f.p_name = request.POST['p_name']
            f.description = request.POST['description']
            f.photo = photo
            f.email = request.user.email
            f.name = request.user.first_name + request.user.last_name
            f.save()
        else:
            return HttpResponse(status=400)
        return redirect('/professional/index/')


@login_required
def view_projects(request):
    projects = Projects.objects.filter(email=request.user.email)
    cat = Categories.objects.all()
    try:
        category = request.GET['category']
    except:
        return render(request, 'view_projects.html', {'projects': projects, 'categories': cat})
    else:
        project_filter = Projects.objects.filter(category_id=category, email=request.user.email)
        return render(request, 'view_projects.html', {'projects': project_filter, 'categories': cat})


@csrf_exempt
@login_required
def update_project(request, pk):
    data = Projects.objects.get(pk=pk)
    if request.method == 'POST':
        image = data.photo
        if not len(request.FILES) == 0:
            if request.FILES:
                filename = request.FILES['photo']
                fs = FileSystemStorage()
                my_file = fs.save(filename.name, filename)
                image = fs.url(my_file)
                image = filename.name
        p_name = request.POST['p_name']
        description = request.POST['description']
        photo = image
        update = Projects(p_id=data.p_id, p_name=p_name, description=description, photo=photo)
        update.save(update_fields=['p_name', 'description', 'photo'])
        return redirect('/professional/view_projects/')
    return render(request, 'update_project.html', {'data': data})


@csrf_exempt
@login_required
def answer_questions(request):
    ques = Questionnaire.objects.filter(p_email=request.user.email, status=0)
    if request.method == 'POST':
        update = Questionnaire(q_id=request.POST['q_id'], answer=request.POST['answer'], status=1)
        update.save(update_fields=['answer', 'status'])
        return redirect('/professional/answer_questions/')
    return render(request, 'answer_questions.html', {'questions': ques})


def delete_project(request, pk):
    if Projects.objects.filter(pk=pk).exists():
        data = Projects.objects.get(pk=pk)
        data.delete()
        return redirect('/professional/view_projects/')
    else:
        return redirect('/professional/view_projects/')