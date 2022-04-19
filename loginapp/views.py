from pprint import pprint
import datetime
import time
from .Google import Create_Service, convert_to_RFC_datetime
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Appointment, Doctor, Patient, Address, Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


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

        try:
            CLIENT_SECRET_FILE = 'loginapp\client_secret.json'
            API_VERSION = 'v3'
            API_NAME = 'calendar'
            SCOPES = ['https://www.googleapis.com/auth/calendar']
            service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        except Exception as e:
            messages.error(
                request, 'Unable to open google calendar consent screen, please try again')
            data = {
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

        if 'profile-picture' in request.FILES:
            try:
                user = User.objects.create_user(username, email, pass1)
                address = Address(line1=addrs, city=city,
                                  state=state, pincode=pin)
                address.save()
                profile = request.FILES['profile-picture']

                if usertype == 'doctor':
                    Doctor(id=user, firstname=firstname, lastname=lastname,
                           profilepic=profile, address=address).save()
                elif usertype == 'patient':
                    Patient(id=user, firstname=firstname, lastname=lastname,
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
                    Doctor(id=user, firstname=firstname,
                           lastname=lastname, address=address).save()
                elif usertype == 'patient':
                    Patient(id=user, firstname=firstname,
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
    if Doctor.objects.filter(id=user).exists():
        doctor = Doctor.objects.get(id=user)
        data = {
            'user': user,
            'child': doctor,
            'usertype': 'Doctor',
            'myposts': Post.objects.filter(owner=doctor).order_by('-id'),
            'posts': Post.objects.filter(status='live').order_by('-id'),
            'appointments': Appointment.objects.filter(doctor=doctor, status='active'),
            'appcount': Appointment.objects.filter(doctor=doctor, status='active').count(),
        }
    elif Patient.objects.filter(id=user).exists():
        appointments = Appointment.objects.filter(patient=Patient.objects.get(id=user), status='active')
        for app in appointments:
            now = time.strftime('%H:%M')
            now_date = datetime.datetime.now().strftime("%Y-%m-%d")

            # print("Time: " + str(app.time), now, str(app.time) < now)
            # print("Date: " + str(app.date), now_date, str(app.date) < now_date)

            if str(app.date) < now_date:
                Appointment.objects.filter(id=app.id).update(status='completed')
            elif str(app.date) == now_date:
                if str(app.time) < now:
                    Appointment.objects.filter(id=app.id).update(status='completed')
        data = {
            'user': user,
            'child': Patient.objects.get(id=user),
            'usertype': 'Patient',
            'posts': Post.objects.filter(status='live').order_by('-id'),
            'doctors': Doctor.objects.all(),
            'appointments': Appointment.objects.filter(patient=Patient.objects.get(id=user), status='active'),
            'appcount': Appointment.objects.filter(patient=Patient.objects.get(id=user), status='active').count(),
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
            doctor = Doctor.objects.get(id=user)
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
            return JsonResponse({'msg': 'error'})
    else:
        if request.method == 'POST':
            title = request.POST.get('title')
            category = request.POST.get('category')
            summary = request.POST.get('summary')
            content = request.POST.get('content')
            status = 'draft'

            if val == 'save-edit':
                status = 'live'

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
            return JsonResponse({'status': 'error', 'msg': 'Something went wrong'})


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
    if Doctor.objects.filter(id=user).exists():
        data = {
            'user': user,
            'child': Doctor.objects.get(id=user),
            'post': post,
            'usertype': 'Doctor',
        }
    elif Patient.objects.filter(id=user).exists():
        data = {
            'user': user,
            'post': post,
            'child': Patient.objects.get(id=user),
            'usertype': 'Patient',
        }
    return render(request, 'postview.html', data)


@login_required(login_url='login')
def bookAppointment(request):
    if request.method == 'POST':
        speciality = request.POST.get('required-speciality')
        date = request.POST.get('app-date')
        time = request.POST.get('app-time')
        username = request.POST.get('doctor-id')
        user = User.objects.get(username=username)
        doc = Doctor.objects.get(id=user)
        patient = Patient.objects.get(id=request.user)

        try:
            entime = datetime.datetime.strptime(time, '%H:%M')
            time = entime
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
            entime = entime + datetime.timedelta(minutes=45)

            Appointment(doctor=doc, patient=patient, time=time,
                        date=date, speciality=speciality, status='active').save()
            doctor_name = 'Dr. ' + doc.firstname + ' ' + doc.lastname
            doctor_email = user.email
            patient_email = request.user.email
            CLIENT_SECRET_FILE = 'loginapp\client_secret.json'
            API_VERSION = 'v3'
            API_NAME = 'calendar'
            SCOPES = ['https://www.googleapis.com/auth/calendar']
            service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
            event = {
                'summary': 'Medical Appointment with ' + doctor_name,
                'description': 'Medical appointment which requires speciality of ' + speciality,
                'start': {
                    # 'dateTime': '2022-04-28T09:00:00-07:00',
                    'dateTime': date.strftime('%Y-%m-%dT') + time.strftime('%H:%M:%S'),
                    'timeZone': 'Asia/Calcutta',
                },
                'end': {
                    'dateTime': date.strftime('%Y-%m-%dT') + entime.strftime('%H:%M:%S'),
                    'timeZone': 'Asia/Calcutta',
                },
                  'attendees': [
                    {'email': doctor_email},
                    {'email': patient_email},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            response = service.events().insert(
                calendarId='primary',
                body=event,
            ).execute()

            # pprint(response)
            message = {
                'status': 'success',
                'name': doc.firstname + ' ' + doc.lastname,
                'date': date.strftime("%B %d, %Y"),
                'sttime': time.strftime('%H:%M %p'),
                'entime': entime.strftime('%H:%M %p'),
            }
            return JsonResponse(message)
        except Exception:
            message = {
                'status': 'error',
                'msg': str(Exception),
            }
            return JsonResponse(message)
    else:
        message = {
            'status': 'error',
            'msg': 'Something went wrong',
        }
        return JsonResponse(message)


@login_required(login_url='login')
def logout_(request):
    logout(request)
    return redirect('login')
