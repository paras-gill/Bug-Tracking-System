from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def developer_home(request):
    return render(request, 'developer/developer_home.html')