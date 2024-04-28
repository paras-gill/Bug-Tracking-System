from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Project, Bug
from django.utils import timezone

@login_required
def manager_home(request):
    projects=Project.objects.all()  # Query set of all projects
    bugs = Bug.objects.all().order_by('project__project_name')  
    bugs_assigned=Bug.objects.filter(assign_to__isnull=False)
    context={'projects' : projects, 'bugs' : bugs, 'bugs_assigned' : bugs_assigned}
    return render(request, 'manager/manager_home.html', context)


@login_required
def manager_project_bugs(request, project_id):
    print(request.user)
    bugs_of_a_project=Bug.objects.filter(project=project_id)
    project_name=Project.objects.get(id=project_id).project_name
    context={
        'bugs_of_a_project' : bugs_of_a_project,
        'project_name' : project_name,
    }
    return render(request, 'manager/manager_project_bugs.html', context)


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
            return redirect('managerHome') 
    else:
        form = forms.AssignBugForm()
    return render(request, 'manager/assign_bug.html', {'form': form})






 