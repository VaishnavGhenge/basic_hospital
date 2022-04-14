from os import stat
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Doctor, Patient, Address, Post
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
                address = Address(line1=addrs, city=city,
                                  state=state, pincode=pin)
                address.save()
                profile = request.FILES['profile-picture']

                if usertype == 'doctor':
                    Doctor(_id=user, firstname=firstname, lastname=lastname,
                           profilepic=profile, address=address).save()
                elif usertype == 'patient':
                    Patient(_id=user, firstname=firstname, lastname=lastname,
                            profilepic=profile, address=address).save()
                messages.success(request, "Account created successfully")
            except Exception as e:
                messages.error(request, e)
        else:
            try:
                user = User.objects.create_user(username, email, pass1)
                address = Address(line1=addrs, city=city,
                                  state=state, pincode=pin)
                address.save()
                if usertype == 'doctor':
                    Doctor(_id=user, firstname=firstname,
                           lastname=lastname, address=address).save()
                elif usertype == 'patient':
                    Patient(_id=user, firstname=firstname,
                            lastname=lastname, address=address).save()
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
        doctor = Doctor.objects.get(_id=user)
        data = {
            'user': user,
            'child': doctor,
            'usertype': 'Doctor',
            'myposts': Post.objects.filter(owner=doctor).order_by('-id'),
            'posts': Post.objects.filter(status='live').order_by('-id'),
        }
    elif Patient.objects.filter(_id=user).exists():
        data = {
            'user': user,
            'child': Patient.objects.get(_id=user),
            'usertype': 'Patient',
            'posts': Post.objects.filter(status='live').order_by('-id'),
        }
    return render(request, 'dashboard.html', data)

@login_required(login_url='login')
def save_post(request, id=0, val='draft'):
    print('inside')
    if id == 0:
        if request.method == 'POST':
            print('inside post')
            title = request.POST.get('title')
            image = request.FILES.get('image')
            category = request.POST.get('category')
            summary = request.POST.get('summary')
            content = request.POST.get('content')
            user = request.user
            doctor = Doctor.objects.get(_id=user)
            status = 'draft'

            if val == 'save':
                status = 'live'

            try:
                Post(owner=doctor, title=title, image=image,
                     category=category, summary=summary, content=content, status=status).save()
                message = {
                    'status': 'success',
                }
                return JsonResponse(message)
            except Exception as e:
                message = {
                    'status': 'error',
                    'msg': e,
                }
                return JsonResponse(message)
        else:
            return JsonResponse({ 'msg': 'error' })
    else:
        if request.method == 'POST':
            title = request.POST.get('title')
            category = request.POST.get('category')
            summary = request.POST.get('summary')
            content = request.POST.get('content')
            status = 'draft'

            if val == 'save-edit':
                status = 'live'

            print(status)
            try:
                if 'image' in request.FILES:
                    image = request.FILES['image']
                    Post.objects.filter(id=id).update(
                    title=title, image=image, category=category, summary=summary, content=content, status=status)
                    message = {
                        'status': 'success',
                    }
                    return JsonResponse(message)
                else:
                    Post.objects.filter(id=id).update(
                    title=title, category=category, summary=summary, content=content, status=status)
                    message = {
                        'status': 'success',
                    }
                    return JsonResponse(message)
            except Exception as e:
                message = {
                    'status': 'error',
                    'msg': e,
                }
                return JsonResponse(message)
        else:
            return JsonResponse({ 'status': 'error', 'msg': 'Something went wrong' })

@login_required(login_url='login')
def delete_post(request, id):
    try:
        Post.objects.filter(id=id).delete()
        message = {
            'status': 'success',
        }
        return JsonResponse(message)
    except Exception as e:
        message = {
            'status': 'error',
            'msg': e,
        }
        return JsonResponse(message)

@login_required(login_url='login')
def postview(request, id):
    user = request.user
    post = Post.objects.get(id=id)
    data = {}
    if Doctor.objects.filter(_id=user).exists():
        data = {
            'user': user,
            'child': Doctor.objects.get(_id=user),
            'post': post,
            'usertype': 'Doctor',
        }
    elif Patient.objects.filter(_id=user).exists():
        data = {
            'user': user,
            'post': post,
            'child': Patient.objects.get(_id=user),
            'usertype': 'Patient',
        }
    return render(request, 'postview.html', data)

@login_required(login_url='login')
def logout_(request):
    logout(request)
    return redirect('login')
