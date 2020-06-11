from django.urls import path
from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("register/", views.UserRegistration.as_view(), name="user_register"),
    path('index/', views.user_index, name='user_index'),
    path('ask_a_question/', views.ask_a_question, name='ask_a_question'),
    path('question/', views.question, name='question'),
    path('answer_questions/', views.answer_questions, name='answer_questions'),
    path('add_review/', views.add_review, name='add_review'),
    path('view_profile/', views.view_profile, name='view_profile'),
]