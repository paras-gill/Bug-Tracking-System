from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . import forms
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from manager.models import Project, Bug



def login_page(request):
    form = forms.LoginForm()
    message = request.session.get("message", None)
    if not message:
        message = ""
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                if user.role == "Developer":
                    return redirect("developerHome")
                elif user.role == "Manager":
                    return redirect("managerHome")

            else:
                message = "Login failed. Incorrect Username or Password!"

    return render(
        request, "authentication/login.html", context={"form": form, "message": message}
    )


def logout_user(request):
    logout(request)
    return redirect("login")


def signup_page(request):
    form = forms.SignupForm()
    if request.method == "POST":
        if not form:
            return render(request, "authentication/signup.html", context={"form": form})
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            form.save()
            request.session["message"] = "Sign Up Successful. Login Here!"
            return redirect("login")
    return render(request, "authentication/signup.html", context={"form": form})


@permission_required("manager.delete_project", raise_exception=True)
def delete_project(request, project_id):
    if request.method == "GET" or request.method == "POST":
        project = get_object_or_404(Project, pk=project_id)
        project.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})

 # 'manager.delete_bug' i.e. user needs the delete_bug permission in the manager app to perform the del op.

@permission_required("manager.delete_bug", raise_exception=True) 
def delete_bug(request, bug_id):
    if not request.user.has_perm("manager.delete_bug"):
        return JsonResponse(
            {"success": False, "error": "Permission denied"}, status=403
        )

    if request.method == "GET" or request.method == "POST":
        bug = Bug.objects.get(id=bug_id)
        bug.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})
