from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from invoice.models import Invoice, InvoiceItem, Customer
from . forms import CreateUser, LoginForm, CustomUserChangeForm

# - Authentication models and functions
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

User=auth.get_user_model()
# Create your views here.
def homepage(request):
    return render(request, 'user/index.html')

def register(request):
    form = CreateUser()

    if request.method=="POST":
        form = CreateUser(request.POST)

        if form.is_valid():

            form.save()

            return redirect("user:login_user")



    context={'registerform':form}

    return render(request, 'user/register.html', context=context)

def login_user(request):
    form = LoginForm()
    if request.method=="POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                print('success')
                return redirect("user:dashboard")
            else:
                return print("Invalid credentials")   

    context={'loginform':form}         
    return render(request, 'user/login.html', context=context)

def logout(request):
    auth.logout(request)
    return redirect("user:login_user")

@login_required(login_url='user:login_user')
def dashboard(request):

    customer_records = Customer.objects.filter(user=request.user)
    context = {'customer_records':customer_records}
    return render(request, 'user/dashboard.html', context=context)


# View Profile
@login_required
def view_profile(request):
    return render(request, 'user/view_profile.html', {'user': request.user})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            return redirect('profile')  # Redirect to a profile page or any other page
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'user/update_profile.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Log out the user before deletion
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('home')  # Redirect to the home page or another suitable location
    
    return render(request, 'user/delete_account.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user:view_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {'form': form})
