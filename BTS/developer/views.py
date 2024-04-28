from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import forms
from manager.models import Project, Bug
from django.db.models import F
from django.utils import timezone



@login_required
def resolve_bug(request, bug_id):
    bug = Bug.objects.get(id=bug_id)
    
    if request.method == 'POST':
        form=forms.ChangeStatusForm(request.POST)
        if form.is_valid():  
            bug.status='Closed'
            project=Project.objects.get(project_name=bug.project.project_name)
            project.bug_count=F('bug_count')-1
            bug.save()
            project.save()
            return render(request, 'developer/success.html', {'bug' : bug})
    else:    
        form=forms.ChangeStatusForm()
    context={
        'bug' : bug,
        'form' : form
    }
    return render (request, 'developer/change_status.html', context)


@login_required
def developer_home(request):
    
    projects=Project.objects.all()  # Query set of all projects
    
    bugs_assigned=Bug.objects.filter(assign_to=request.user.pk)
    bugs_assigned_open=Bug.objects.filter(assign_to=request.user.pk, status='Open')
    
    bugs_submitted=Bug.objects.filter(submitted_by=request.user.pk)
    bugs_submitted_open=Bug.objects.filter(submitted_by=request.user.pk, status='Open')
    
    message=''
    context={
        'projects' : projects, 
        'bugs_assigned' : bugs_assigned, 
        'bugs_assigned_open' : bugs_assigned_open,
        'bugs_submitted' : bugs_submitted,
        'bugs_submitted_open' : bugs_submitted_open, 
        'message' : message
        }
               
    return render(request, 'developer/developer_home.html', context)


@login_required
def file_bug(request):
    message=''
    if request.method == 'POST':
        form = forms.BugForm(request.POST)
        if form.is_valid():
            bug=form.save(commit=False) 
            bug.submitted_by = request.user  
            bug.date_submitted = timezone.now().date()  
            bug.save()
            project = bug.project
            Project.objects.filter(id=project.id).update(bug_count=F('bug_count') + 1)
            message=f" <span style='color:blue;'> Bug with title <b>{bug.bug_title}</b> successfully filed for <b>{bug.project}</b> project </span>"
        else:
            message='<span style="color:red;"> A bug with this title already exists in the selected project.</span>'

    form = forms.BugForm()
    return render(request, 'developer/file_bug.html', {'form': form, 'message' : message})


@login_required
def developer_project_bugs(request, project_id ):
    bugs_of_a_project=Bug.objects.filter(project=project_id)
    project_name=Project.objects.get(id=project_id).project_name
    user=request.user
    context={
        'bugs_of_a_project' : bugs_of_a_project,
        'project_name' : project_name,
        'user' : user
    }
    return render(request, 'developer/developer_project_bugs.html', context)