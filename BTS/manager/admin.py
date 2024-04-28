from django.contrib import admin

from .models import Project, Bug

admin.site.register(Project)
admin.site.register(Bug)