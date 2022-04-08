from genericpath import exists
from django.shortcuts import redirect, render
from .models import Doctor, Patient, Address
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        usertype = request.POST.get('usertype')
        addrs = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin = request.POST.get('pincode')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username taken please try new')
            if 'profile-picture' in request.FILES:
                profile = request.FILES['profile-picture']
            else:
                profile = None
            data = {
                'profile_picture': profile,
                'firstname': firstname,
                'lastname': lastname,
                'usertype': usertype,
                'addrs': addrs,
                'city': city,
                'state': state,
                'pin': pin,
                'email': email,
                'pass1': pass1,
                'pass2': pass2,
            }
            return render(request, 'signup.html', data)

        if pass1 != pass2:
            messages.error(request, 'Password is not matching')
            if 'profile-picture' in request.FILES:
                profile = request.FILES['profile-picture']
            else:
                profile = None
            data = {
                'profile_picture': profile,
                'firstname': firstname,
                'lastname': lastname,
                'usertype': usertype,
                'addrs': addrs,
                'city': city,
                'state': state,
                'pin': pin,
                'email': email,
                'pass1': pass1,
            }
            return render(request, 'signup.html', data)

        if 'profile-picture' in request.FILES:
            try:
                user = User.objects.create_user(username, email, pass1)
                address = Address(line1=addrs, city=city, state=state, pincode=pin)
                address.save()
                profile = request.FILES['profile-picture']

                if usertype == 'doctor':
                    Doctor(_id=user, firstname=firstname, lastname=lastname, profilepic=profile, address=address).save()
                elif usertype == 'patient':
                    Patient(_id=user, firstname=firstname, lastname=lastname, profilepic=profile, address=address).save()
                messages.success(request, "Account created successfully")
            except Exception as e:
                messages.error(request, e)
        else:
            try:
                user = User.objects.create_user(username, email, pass1)
                address = Address(line1=addrs, city=city, state=state, pincode=pin)
                address.save()
                if usertype == 'doctor':
                    Doctor(_id=user, firstname=firstname, lastname=lastname, address=address).save()
                elif usertype == 'patient':
                    Patient(_id=user, firstname=firstname, lastname=lastname, address=address).save()
                messages.success(request, "Account created successfully")
            except Exception as e:
                messages.error(request, e)
        return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')

def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'User not found')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

@login_required(login_url='login')
def dashboard(request):
    user = request.user
    data = {}
    if Doctor.objects.filter(_id=user).exists():
        data = {
            'user': user,
            'child': Doctor.objects.get(_id=user),
            'usertype': 'Doctor',
        }
    elif Patient.objects.filter(_id=user).exists():
        data = {
            'user': user,
            'child': Patient.objects.get(_id=user),
            'usertype': 'Patient',
        }
    return render(request, 'dashboard.html', data)

def logout_(request):
    logout(request)
    return redirect('login')