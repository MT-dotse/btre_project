import email

from django.contrib import auth, messages

# from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from contacts.models import Contact

from .forms import RegisterUserForm

# from django.contrib.auth import authenticate, login


# View methods
def register(request):
    if request.method == "POST":
        # Create object of form
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You are now registered and can log in")
            return redirect("login")
        else:
            return redirect("register")
    else:
        return render(request, "accounts/register.html")


def login(request):
    if request.method == "POST":
        # Login User
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")

    else:
        return render(request, "accounts/login.html")


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, "You are now logged out")
        return redirect("index")


def dashboard(request):
    user_contacts = Contact.objects.order_by("-contact_date").filter(
        user_id=request.user.id
    )
    context = {"contacts": user_contacts}
    return render(request, "accounts/dashboard.html", context)
