from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Room, Topic, Messages
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    #pagination
    paginator = Paginator(rooms, 2)  # posts per page
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)


    topics =Topic.objects.all()
    room_count = rooms.count()

    #activities
    room_msgs = Messages.objects.filter(Q(room__topic__name__icontains=q)).order_by('-created')


    context = {'rooms':queryset,'topics':topics,'room_count':room_count,'room_msgs':room_msgs}
    return render(request,"./base/home.html",context)

def room(request,pk):
    room =Room.objects.get(id=int(pk))

    #comments
    room_messages = room.messages_set.all().order_by('-created') # give msgs related to this room model name messages

    #participants
    participants = room.participants.all()
    print(participants)

    if request.method=='POST':
        message = Messages.objects.create(
            user =request.user,
            room =room,
            body =request.POST.get('body')
        )

        room.participants.add(request.user)
        return redirect('room',pk=room.id)


    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request, "./base/room.html", context)


def userProfile(request,pk):
    user =User.objects.get(id=int(pk))
    rooms = user.room_set.all()
    # activities
    room_msgs = user.messages_set.all()
    topics =Topic.objects.all()

    context={'user':user,'rooms':rooms,'room_msgs':room_msgs,'topics':topics}
    return render(request,'./base/profile.html',context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    if request.method=='POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, "./base/room_form.html", context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room =Room.objects.get(id=int(pk))
    form=RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed')
    if request.method == 'POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'./base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=int(pk))

    if request.user != room.host:
        return HttpResponse('you are not allowed.')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'./base/delete.html',{'obj':room})


def userlogin(request):
    page ='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            #User inbuild table
            user = User.objects.get(username=username)
        except:
            #flash messages
            messages.error(request,'No user exist')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            #login method creates a session
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or Password does not exist')


    context={'page':page}
    return render(request,'./base/login_register.html',context)

def userlogout(request):
    logout(request)
    return redirect('home')

def registeruser(request):
    page ='register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registeration')
    context={'page':page,'form':form}
    return render(request,'./base/login_register.html',context)


@login_required(login_url='login')
def deleteMsg(request,pk):
    msg=Messages.objects.get(id=pk)

    if request.user != msg.user:
        return HttpResponse('you are not allowed.')

    if request.method == 'POST':
        msg.delete()
        return redirect('home')
    return render(request,'./base/delete.html',{'obj':msg})

