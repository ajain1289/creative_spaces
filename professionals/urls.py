from django.urls import path
from professionals.apps import ProfessionalsConfig
from professionals import views


app_name = ProfessionalsConfig.name

urlpatterns =[
    path('registration/', views.ProfessionalRegistration.as_view(), name='professional_registration'),
    path('index/', views.professional_index, name='professional_index'),
    path('add_project/', views.AddProject.as_view(), name='add_project'),
    path('view_projects/', views.view_projects, name='view_projects'),
    path('answer_questions/', views.answer_questions, name='answer_questions'),
    path('update_project/<int:pk>/', views.update_project, name='update_project'),
    path('delete_project/<int:pk>/', views.delete_project, name='delete_project')
]