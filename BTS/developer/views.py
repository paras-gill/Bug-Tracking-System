from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from manager.models import Project, Bug
from django.db.models import F
from django.utils import timezone
from django.forms import formset_factory

@login_required
def developer_home(request):
    
    projects=Project.objects.all()  # Query set of all projects
    
    bugs_assigned=Bug.objects.filter(assign_to=request.user.pk)
    bugs_assigned_open=Bug.objects.filter(assign_to=request.user.pk, status='Open')
    
    bugs_submitted=Bug.objects.filter(submitted_by=request.user.pk)
    bugs_submitted_open=Bug.objects.filter(submitted_by=request.user.pk, status='Open')
      
    ChangeStatusFormSet = formset_factory(forms.ChangeStatusForm, extra=len(bugs_assigned))
    formset = ChangeStatusFormSet() 
    
    zipped_bugsassigned_formset=zip(bugs_assigned, formset)
    context={
        'projects' : projects, 
        'bugs_assigned' : bugs_assigned, 
        'bugs_assigned_open' : bugs_assigned_open,
        'bugs_submitted' : bugs_submitted,
        'bugs_submitted_open' : bugs_submitted_open,
        'zipped_bugsassigned_formset' : zipped_bugsassigned_formset
        }
    
    message=''

    if request.method == 'GET':           
        return render(request, 'developer/developer_home.html', context)
    
    elif request.method=='POST':
        formset = ChangeStatusFormSet(request.POST)  # Binding the POST data to the formset
        #print(formset.is_valid())

        if formset.is_valid():
            closed_count=0  # Count of closed bug status
            for bug, form in zip(bugs_assigned, formset):
                if form.clean['resolve']==True:  # i.e. when checkbox checked, then we have to update its status 
                    closed_count+=1
                    bug.update(status='Closed')
                    project=Project.objects.get(pk=bug.project)
                    project.update(bug_count=F('bug_count')-1)
                    
            if closed_count == 1:
                message = f"{closed_count} bug has been resolved"
            else:
                message = f"{closed_count} bugs have been resolved"
        
        else:
            print('formset is invalid')
        
        '''
        else:
            # Formset is invalid, handle errors
            print('formset is invalid')
            for form in formset:
                if form.errors:
                    # Access errors for the current form
                    print(form.errors)
        '''

        context['message']=message
        return render(request, 'developer/developer_home.html', context)



@login_required
def file_bug(request):
    message=''
    if request.method == 'POST':
        form = forms.BugForm(request.POST)
        if form.is_valid():
            bug=form.save(commit=False) # commit=False because we want to modify the object beofre saving.
            bug.submitted_by = request.user  # Set the submitted_by field to the current user object (bcoz it is a foreign key)
            bug.date_submitted = timezone.now().date()  # Set the date_submitted field to the current date without timestamp
            bug.save()
            project = bug.project
            Project.objects.filter(id=project.id).update(bug_count=F('bug_count') + 1)
            message=f" <span style='color:blue;'> Bug with title <b>{bug.bug_title}</b> successfully filed for <b>{bug.project}</b> project </span>"
        else:
            message='<span style="color:red;"> A bug with this title already exists in the selected project.</span>'

    form = forms.BugForm()
    return render(request, 'developer/file_bug.html', {'form': form, 'message' : message})

@login_required
def change_status(request):
    pass
    #return redirect('developerHome')



