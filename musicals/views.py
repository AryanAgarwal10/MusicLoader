from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from musicals.forms import MusicForm
from musicals.models import Access, Music

# Create your views here.
def home(request):
    return render(request, "musicals/index.html")

def signup(request):
    if request.method == "POST":
       email = request.POST.get("email")
       username = request.POST.get("email")
       password = request.POST.get("password")
       user = User.objects.get(email=email)
       if user is not None:
         messages.error(request, "User already exists")
         return redirect('signup')        
       user = User.objects.create_user(username, email, password)
       user.save()
       
       messages.success(request, "Account created successfully")
       
       return redirect('signin')


    return render(request, "musicals/signup.html")

def signin(request):
    if request.method == "POST":
       email = request.POST.get("email")
       password = request.POST.get("password")
       
       user = authenticate(username=email, password=password)
      
       if user is not None:
         login(request, user)
         print("Login successful")
         messages.success(request, "Login successful")
         request.session['email'] = email
         request
         return render(request,"musicals/index.html",{"email":email})
       
       else:
        print("Invalid credentials")
       
        messages.error(request, "Invalid credentials")
        return redirect('signin')
          
    return render(request, "musicals/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')




def add(request):
    if request.session.has_key('email'):
      email = request.session['email']
    else:
        return redirect('home')
    

    if request.method=='POST':
       form=MusicForm(request.POST, request.FILES)
       if form.is_valid():
          music=form.cleaned_data['music']
          type=form.cleaned_data['type']
          title=form.cleaned_data['title']
          owner=User.objects.get(email=email).id
          
          audio=Music(title=title,music=music,owner=owner,type=type)
          if type=='protected':
            emails=request.POST.get('emails')
            emails=emails.split("\n")
            for email in emails:
              access=Access(email=email,music=audio)
              access.save()
          audio.save()
       
    else:
         form=MusicForm()
    
    return render(request, "musicals/add.html",{'form':form})

def viewMusic(request):
   email=request.session['email']
   owner=User.objects.get(email=email).id
   publicMusic=list(Music.objects.filter(type='public'))
   
   privateMusic=list(Music.objects.filter(type='private', owner=owner))
   
   accessibleMusic=list(Access.objects.filter(email=email).values_list('music', flat=True).order_by('id'))
   
   music=publicMusic+privateMusic+accessibleMusic

   return render(request, "musicals/viewMusic.html",{'music':music})