from django.shortcuts import render,redirect
from .models import Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):   
    return render(request,'home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,
                                    password=password)
        if user is not None:
            login(request,user)
            print("Login Successful")
            return redirect('home')
        else:
            error_message = "Invalid Login"
            print(error_message)
    return render(request,'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        User.objects.create_user(username=username,
                                 password=password)
        new_profile = Profile(username=username,
                              password=password,
                              firstname=firstname,
                              lastname=lastname,
                              email=email,
                              user = User.objects.get(username=username))
        new_profile.save()
        print("User Created Successfully")
        return redirect('home')
    return render(request,'register.html')

@login_required(login_url='login')
def  transfer(request):
    if request.method == 'POST':
        sender = request.user.username
        receiver = request.POST.get('receiver')
        amount = request.POST.get('amount')
        amount = float(amount)
        sender_profile = Profile.objects.get(username=sender)
        receiver_profile = Profile.objects.get(username=receiver)
        receiver_exists = Profile.objects.filter(username=receiver).exists()
        print(f'{sender}-->{receiver}-->Rs.{amount}')
        if receiver_exists:
            if amount>sender_profile.balance:
                error = "No Sufficient Balance"
                print(error)
            else:
                receiver_profile.balance = receiver_profile.balance + amount
                sender_profile.balance = sender_profile.balance - amount
                receiver_profile.save()
                sender_profile.save()
        else:
            error = "Receiver Not Found"
            print(error)
    return render(request,'transfer.html')

