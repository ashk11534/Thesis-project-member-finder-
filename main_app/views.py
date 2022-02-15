from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import RoomForm
from .forms import SignupForm, UpdateProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import RoomMessage, University, User, Room, UserMessage
from django.contrib import messages
from django.db.models import Q

# Create your views here.

def index(request):
    users = None
    rooms = None
    topic = request.GET.get('topic') if request.GET.get('topic') != None else ''
    user_id = request.GET.get('id')
    if user_id:
        user_id = int(user_id)
        rooms = Room.objects.filter(host__id=user_id).order_by('-created_at')
    else:
        rooms = Room.objects.filter(
            Q(tag__name__icontains=topic) | 
            Q(name__icontains=topic)| 
            Q(description__icontains=topic)|
            Q(host__id=user_id)).order_by('-created_at')
    room_count = rooms.count()
    all_rooms = Room.objects.count()
    thesis_count = Room.objects.filter(tag__name='Thesis').count()
    project_count = Room.objects.filter(tag__name='Project').count()
    if request.user.is_authenticated:
        users = User.objects.filter(university=request.user.university)
    else:
        users = User.objects.filter().order_by('-id')[0:4]
    return render(request, 'main_app/index.html', {
            'users': users, 
            'rooms': rooms, 
            'room_count': room_count,
            'all_rooms': all_rooms,
            'thesis_count': thesis_count,
            'project_count': project_count
        })

def user_signup(request):
    signup_form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'main_app/signup.html', {'signup_form': form})
    return render(request, 'main_app/signup.html', {'signup_form': signup_form})

def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    rooms = Room.objects.filter(host=user)
    all_rooms = Room.objects.all()
    return render(request, 'main_app/user-profile.html', {'user': user, 'rooms': rooms, 'all_rooms':all_rooms})

@login_required(login_url='login')
def update_profile(request, page_name):
    profile = request.user
    update_profile_form = UpdateProfileForm(instance=profile)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            if page_name == 'index':
                return redirect('home')
            elif page_name == 'profile':
                return redirect('user-profile', request.user.id)
        else:
            return render(request, 'main_app/update-profile.html', {'update_profile_form': form, 'page_name': page_name})
    return render(request, 'main_app/update-profile.html', {'update_profile_form': update_profile_form, 'page_name': page_name})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
            return redirect('login')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong email or password')
            return redirect('login')
    return render(request, 'main_app/login.html')

@login_required(login_url='login')
def create_room(request, user_id, page_name):
    room_form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            tag = form.cleaned_data.get('tag')
            description = form.cleaned_data.get('description')
            room = Room.objects.create(name=name, tag=tag, description=description, host=request.user)
            room.participants.add(request.user)
            room.save()
            if page_name == 'index':
                return redirect('home')
            elif page_name == 'profile':
                return redirect('user-profile', user_id)
        else:
            return render(request, 'main_app/create-room.html', {'room_form': form, 'user_id': user_id, 'page_name': page_name})
    return render(request, 'main_app/create-room.html', {'room_form': room_form, 'user_id': user_id, 'page_name': page_name})

def room(request, room_id):
    single_room = Room.objects.get(id=room_id)
    participants = single_room.participants.all()
    room_messages = RoomMessage.objects.filter(room=single_room).order_by('-id')
    return render(request, 'main_app/room.html', {'single_room': single_room, 'participants': participants, 'room_messages': room_messages})

@login_required(login_url='login')
def join_room(request, room_id, user_id):
    room = Room.objects.get(id=room_id)
    user = User.objects.get(id=user_id)

    room.participants.add(user)
    room.save()
    return redirect('room', room.id)

@login_required(login_url='login')
def send_message(request):
    room_id = request.POST.get('room_id')
    user_id = request.POST.get('user_id')
    room = Room.objects.get(id=room_id)
    user = User.objects.get(id=user_id)
    message_body = request.POST.get('message')

    message = RoomMessage(sender=user, body=message_body, room=room)
    message.save()
    return redirect('room', room.id)

@login_required(login_url='login')
def delete_message(request, message_id, room_id):
    message = RoomMessage.objects.get(id=message_id)
    message.delete()
    return redirect('room', room_id)

@login_required(login_url='login')
def delete_user_message(request, message_id, user_id):
    user = User.objects.get(id=user_id)
    message = UserMessage.objects.get(receiver=user, id=message_id)
    message.delete()

    return redirect('received-messages', user_id)

@login_required(login_url='login')
def delete_all_user_message(request, user_id):
    user = User.objects.get(id=user_id)
    UserMessage.objects.filter(receiver=user).delete()
    
    return redirect('received-messages', user_id)

@login_required(login_url='login')
def user_message(request, sender_id, receiver_id):
    if request.method == 'POST':
        message = request.POST.get('sender-message')
        sender_id = sender_id
        receiver_id = receiver_id

        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)

        sent_message = UserMessage(sender=sender, receiver=receiver, body=message)
        sent_message.save()
        messages.success(request, f'Message is received by @{receiver.username}')
        return redirect('user-message', sender_id, receiver_id)
    return render(request, 'main_app/user-message.html', {
        'sender_id': sender_id,
        'receiver_id': receiver_id
    })

@login_required(login_url='login')
def received_messages(request, user_id):
    user = User.objects.get(id=user_id)
    messages = UserMessage.objects.filter(receiver=user).order_by('-id')
    return render(request, 'main_app/received-message.html', {'messages': messages})

@login_required(login_url='login')
def update_room(request, room_id):
    room = Room.objects.get(id=room_id)
    room_form = RoomForm(instance=room)
    if request.method == 'POST':
        update_form = RoomForm(request.POST, instance=room)
        if update_form.is_valid():
            update_form.save()
            return redirect('home')
        else:
            return render(request, 'main_app/update-room.html', {'room_id':room_id, 'room_form': update_form})
    return render(request, 'main_app/update-room.html', {'room_id':room_id, 'room_form': room_form})

@login_required(login_url='login')
def delete_room(request, id, user_id, page_name):
    room = Room.objects.get(id=id)
    room.delete()
    if page_name == 'index':
        return redirect('home')
    elif page_name == 'profile':
        return redirect('user-profile', user_id)
@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('home')