from django import forms
from professionals.models import Projects


class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Projects
        exclude = ['p_id', 'p_name', 'category', 'email', 'description', 'photo', 'name']