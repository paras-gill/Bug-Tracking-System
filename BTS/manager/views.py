from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Project, Bug

@login_required
def manager_home(request):
    projects=Project.objects.all()  # Query set of all projects
    bugs = Bug.objects.all().order_by('project__project_name')  # '__' is used to navigate the relationship between the Bug model and the Project model.
    #bugs=Bug.objects.all()
    context={'projects' : projects, 'bugs' : bugs}
    return render(request, 'manager/manager_home.html', context)

@login_required
def upload_project(request):
    if request.method == 'POST':
        form = forms.UploadProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('managerHome') 
    else:
        form = forms.UploadProjectForm()
    return render(request, 'manager/upload_project.html', {'form': form})






 