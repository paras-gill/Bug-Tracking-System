"""
URL configuration for BTS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

import authentication.views
import developer.views  
import manager.views

urlpatterns = [
    # Authentication URL endpoints
    path('', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('deleteProject/<int:project_id>/', authentication.views.delete_project, name='deleteProject'),
    path('deleteBug/<int:bug_id>/', authentication.views.delete_bug, name='deleteBug'),

    # Manager URL endpoints
    path('managerHome/', manager.views.manager_home, name='managerHome'),
    path('managerHome/uploadProject', manager.views.upload_project, name='uploadProject'),
    path('managerHome/assignBug', manager.views.assign_bug, name='assignBug'),
    path('managerHome/projectBugs/<int:project_id>/', manager.views.manager_project_bugs, name='manager_projectBugs'),

    # Developer URL endpoints
    path('developerHome/', developer.views.developer_home, name='developerHome'),
    path('developerHome/fileBug', developer.views.file_bug, name='fileBug'),  
    path('developerHome/resolve/<int:bug_id>/', developer.views.resolve_bug, name='resolveBug'),
    path('developerHome/projectBugs/<int:project_id>/', developer.views.developer_project_bugs, name='developer_projectBugs'),
]
