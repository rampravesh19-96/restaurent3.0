from django.shortcuts import render,HttpResponse
from django.shortcuts import redirect
from datetime import datetime
import requests
import json
from django.http import JsonResponse
from myapp.models import User
import jwt,os
from dotenv import load_dotenv
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_folder = os.path.expanduser(BASE_DIR) 
load_dotenv(os.path.join(project_folder, '.env'))

# Create your views here.


def home(request):
   try:
      token=request.COOKIES.get('token')
      if not token:
         return redirect("/login")
      id=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"] 
      userObj=User.objects.filter(id=id)
      if len(userObj)==0:
         return redirect("/login")
      return render(request,"home.html")
   except:
      return redirect("/login")



def register(request):
   return render(request,'register.html')

def login(request):
   response=render(request,'login.html')
   return response

def forgotPassword(request):
   return render(request,'forgot_password.html')
   
def savePassword(request):
   try:
      token=request.GET['token'].replace("'","")[1:]
      print(token)
      id=jwt.decode(token, os.getenv("RESET_PASSWORD_SECRET_KEY"), algorithms=["HS256"])["id"] 
      return render(request,'save_password.html')
   except:
      redirect("/login")

def viewItem(request):
   try:
      token=request.COOKIES.get('token')
      if not token:
         return redirect("/login")
      id=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"] 
      userObj=User.objects.filter(id=id)
      if len(userObj)==0:
         return redirect("/login")
      return render(request,"view_item.html")
   except:
      return redirect("/login")
def checkout(request):
   try:
      token=request.COOKIES.get('token')
      if not token:
         return redirect("/login")
      id=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"] 
      userObj=User.objects.filter(id=id)
      if len(userObj)==0:
         return redirect("/login")
      return render(request,"checkout.html")
   except:
      return redirect("/login")

def orderHistoryForUser(request):
   try:
      token=request.COOKIES.get('token')
      if not token:
         return redirect("/login")
      id=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"] 
      userObj=User.objects.filter(id=id)
      if len(userObj)==0:
         return redirect("/login")
      return render(request,"order_history_for_user.html")
   except:
      return redirect("/login")


def editUserProfile(request):
   try:
      token=request.COOKIES.get('token')
      if not token:
         return redirect("/login")
      id=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"] 
      userObj=User.objects.filter(id=id)
      if len(userObj)==0:
         return redirect("/login")
      return render(request,"edit_user_profile.html")
   except:
      return redirect("/login")
   

def admin(request):
   try:
      token=request.COOKIES.get('token')
      if not token:
         return redirect("/login")
      id=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"] 
      userObj=User.objects.filter(id=id)
      if len(userObj)==0:
         return redirect("/login")
      return render(request,"admin.html")
   except:
      return redirect("/login")
def orderHistoryAdmin(request):
   try:
      token=request.COOKIES.get('token')
      if not token:
         return redirect("/login")
      id=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"] 
      userObj=User.objects.filter(id=id)
      if len(userObj)==0:
         return redirect("/login")
      return render(request,"order_history_for_admin.html")
   except:
      return redirect("/login")



