from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def register(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            NFUO=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            NFUO.set_password(password)
            NFUO.save()

            NFPO=pfd.save(commit=False)
            NFPO.username=NFUO
            NFPO.save()
            return HttpResponse('Registeration successfully done....')
        else:
            return HttpResponse('Not valid....')
    return render(request,'registeration.html',d)

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid....')
    return render(request,'login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO) 
    d={'UO':UO,'PO':PO}
    return render(request,'display_profile.html',d)