from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Project, Bug
from django.utils import timezone

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

@login_required
def assign_bug(request):
    if request.method == 'POST':
        form = forms.AssignBugForm(request.POST)
        if form.is_valid():
            bug=Bug.objects.get(pk=request.POST['project_bug'])
            bug.assign_to = form.cleaned_data['assigned_to']
            bug.date_assigned = timezone.now()
            bug.save()
            #project = bug.project
            #Project.objects.filter(id=project.id).update(bug_count=F('bug_count') + 1)
            return redirect('managerHome') 
    else:
        form = forms.AssignBugForm()
    return render(request, 'manager/assign_bug.html', {'form': form})






 