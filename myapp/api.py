from .validate import validateEmail,validatePassword,validateDob,isFloat
from myapp.models import User,Customer,Product,Orders,OrderDetails,Cart
from restaurant.insert_into import insert_into
from django.db.models import Max,Count,Sum
from datetime import datetime,timedelta
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core import serializers
from django.db import transaction
from .send_email import sendEmail
import hashlib,random,json,jwt,os
from  django.db.models import Q
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_folder = os.path.expanduser(BASE_DIR) 
load_dotenv(os.path.join(project_folder, '.env'))
import requests
from django.db.models import Count, F, Value

def register(request):
   try:
      if not request.POST:
         return JsonResponse({"status":"failure", "message":"Invalid request", "data":None})
      token=request.COOKIES.get('token')
      if token:
         return JsonResponse({"status":"success", "message":"You are already registered", "data":{"url":"/login"}})

      email = request.POST.get('email')
      name = request.POST.get('name')
      password=request.POST.get('password')
      confirmPassword=request.POST.get('confirmPassword')
      phone=request.POST.get('phone')
      dob=request.POST.get('dob')
      address=request.POST.get('address')
      
      if not email or not name or not password or not confirmPassword or not phone or not dob or not address:
         return JsonResponse({"status":"failure", "message":"All fields are required", "data":None})
      if not validateEmail(email):
         return JsonResponse({"status":"failure", "message":"Invalid email", "data":None})
      if not len(phone)==10 or not phone.isdigit():
         return JsonResponse({"status":"failure", "message":"Invalid phone number", "data":None})
      if not validateDob(dob):
         return JsonResponse({"status":"failure", "message":"Dob must be in format 'Y-M-D'", "data":None})
      if len(address)<25 or len(address)>500:
         return JsonResponse({"status":"failure", "message":"Address must be between 15 to 500 characters", "data":None})
      if password !=confirmPassword:
         return JsonResponse({"status":"failure", "message":"Pasword did not match", "data":None})
      if not validatePassword(password):
         return JsonResponse({"status":"failure", "message":"Password must have atleast 8 character,uppercase,lower case, number and special character", "data":None})
      hashedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
      data=User.objects.filter(email=email)
      if len(data)==0:
         with transaction.atomic():
            userObj = User(email=email, password=hashedPassword,name=name)
            userObj.save()
            customerObj=Customer(idd=userObj,phone=phone,dob=dob,address=address)
            customerObj.save() 
            cartObj=Cart(customer_id=userObj.id)
            cartObj.save()
         return JsonResponse({"status":"success", "message":"User created successfully", "data":{"url":"/login"}})    
      else:
         return JsonResponse({"status":"failure", "message":"Email is already registered", "data":None})
   except:
      return JsonResponse({"status":"failure", "message":"An error occurred", "data":None})


def verifyUser(request):
   try:
      token=request.COOKIES.get('token')
      print(token)
      if not token:
         return JsonResponse({"status":"failure", "message":"Aunthentication failed", "data":{"url":"/login"}})
      id=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"]   
      userObj=User.objects.filter(id=id)
      if len(userObj)==0:
         return JsonResponse({"status":"success", "message":"Aunthentication failed", "data":{"url":"/login"}})
      return None
   except:
      return JsonResponse({"status":"success", "message":"Aunthentication failed", "data":{"url":"/login"}})




def login(request):
   try:
      if not request.POST:
         return JsonResponse({"status":"failure", "message":"Invalid request", "data":None})
      token=request.COOKIES.get('token')
      
      if token:
         isAdmin=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])['is_admin']
         url="/"
         if isAdmin:
            url="/admin"
         return JsonResponse({"status":"success", "message":"You are already log in", "data":{"url":url}})

      email = request.POST.get('email')
      password = request.POST.get('password')
      if not email or not password:
         return JsonResponse({"status":"failure", "message":"All fields are required", "data":None})
      hashedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
      data=User.objects.values_list("id","email","password","is_admin","name").filter(email=email,password=hashedPassword)
      if len(data)==0:
         return JsonResponse({"status":"failure", "message":"Invalid user id or password", "data":None})
      payload={
            'id':data[0][0],
            'is_admin':data[0][3]
        }
 
      token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256").decode('utf-8')
      url="/"
      if data[0][3]:
         url="/admin"
      response=JsonResponse({"status":"success", "message":"Successfully logged in", "data":{"token":str(token),"url":url}})
      response.set_cookie(key='token',value=token,max_age = 100000, expires = None)
      response.cookies['token']['expires'] = datetime.today() + timedelta(days= 1) 
      return response
   except:
      return JsonResponse({"status":"failure", "message":"An error occurred", "data":None})
   

         



def forgotPassword(request):
   try:
      if not request.POST:
         return JsonResponse({"status":"failure", "message":"Invalid request", "data":None})
      email = request.POST.get('email')
      if not email:
         return JsonResponse({"status":"failure", "message":"Email is required", "data":None})
      data=User.objects.values_list("id","email").filter(email=email)
      if len(data)==0:
         return JsonResponse({"status":"success", "message":"This email is not registered", "data":None})
      token = jwt.encode({"id": data[0][0]}, os.getenv("RESET_PASSWORD_SECRET_KEY"), algorithm="HS256")
      otp=random.randint(100000,999999)
      current_date_time = datetime.now().replace(microsecond=0)
      with transaction.atomic(): 
         data.update(password_reset_otp=otp,password_reset_otp_time=current_date_time)
      if not sendEmail(email,"Reset password OTP",otp):
         return JsonResponse({"status":"success", "message":"Something went wrong", "data":None})
      return JsonResponse({"status":"success", "message":"Email sent successfully", "data":{"url":"/save-password?token="+str(token)}})
   except:
      return JsonResponse({"status":"failure", "message":"An error occurred", "data":None})




def savePassword(request):
   try:
      if not request.POST:
         return JsonResponse({"status":"failure", "message":"Invalid request", "data":None})
      token=request.POST.get('token')
      token=token.replace("'","")[1:]
      print(token)
      if not token:
         return JsonResponse({"status":"failure", "message":"Unable to validate request", "data":None})
      id=jwt.decode(token, os.getenv("RESET_PASSWORD_SECRET_KEY"), algorithms=["HS256"])["id"] 
      otp = request.POST.get('otp')
      password=request.POST.get('password')
      confirmPassword=request.POST.get('confirmPassword')
      if not otp or not password or not confirmPassword:
         return JsonResponse({"status":"failure", "message":"All fields are required", "data":None})
      if not password==confirmPassword:
         return JsonResponse({"status":"failure", "message":"Password did not match", "data":None})
      if not validatePassword(password):
         return JsonResponse({"status":"failure", "message":"Password must have atleast 8 character,uppercase,lower case, number and special character", "data":None})
      data=User.objects.values_list("password_reset_otp","password_reset_otp_time").filter(id=id)
      if data[0][0]!=otp:
         return JsonResponse({"status":"failure", "message":"Invalid OTP", "data":None})
      current_date_time = datetime.now().replace(microsecond=0) 
      difference = current_date_time - data[0][1].replace(tzinfo=None
      )
      if difference > timedelta(seconds=0, minutes=1, hours=0):
         return JsonResponse({"status":"success", "message":"OTP expired", "data":None})
      hashedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
      with transaction.atomic():
         data.update(password=hashedPassword)
      return JsonResponse({"status":"success", "message":"Password reset successfully", "data":{"url":"/login"}})
   except:
      return JsonResponse({"status":"failure", "message":"An error occurred", "data":None})



def editUserProfile(request):
   try:
      if not request.POST:
         return JsonResponse({"status":"failure", "message":"Invalid request", "data":None})
      response=verifyUser(request)
      if response is not None:
         return response
      token=request.COOKIES.get('token')
      if not token:
         return JsonResponse({"status":"failure", "message":"Unable to validate request", "data":None})
      id=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"] 
      name=request.POST.get('name')
      phone=request.POST.get('phone')
      dob=request.POST.get('dob')
      address=request.POST.get('address')
      if not id or not name or not phone or not dob:
         return JsonResponse({"status":"failure", "message":"All fields are required", "data":None})
      if not len(phone)==10 or not phone.isdigit():
         return JsonResponse({"status":"failure", "message":"Invalid phone number", "data":None})
      if not validateDob(dob):
         return JsonResponse({"status":"failure", "message":"Dob must be in format 'Y-M-D'", "data":None})
      if len(address)<25 or len(address)>500:
         return JsonResponse({"status":"failure", "message":"Address must be between 15 to 500 characters", "data":None})
      with transaction.atomic():
         User.objects.filter(id=id).update(name=name)
         Customer.objects.filter(id=id).update(phone=phone,dob=dob,address=address)
      return JsonResponse({"status":"success", "message":"User profile updated", "data":{"id":id}})
   except:
      return JsonResponse({"status":"failure", "message":"An error occurred", "data":None})
      


def viewItemList(request):
   try:
      if False:
         return JsonResponse({"status":"failure", "message":"Invalid request", "data":None})
      page=request.POST.get('page')
      query=request.POST.get('query')
      minPrice=request.POST.get('min_price')
      maxPrice=request.POST.get('max_price')
      noOfProductPerPage=request.POST.get('no_of_product_per_page')
      print(noOfProductPerPage)
      if not page:
         page="1"
      if not query:
         query=""
      if not minPrice:
         minPrice=os.getenv("MIN_PRICE")
      if not maxPrice:
         maxPrice=os.getenv("MAX_PRICE")
      if not page.isdigit() or not minPrice.isdigit() or not maxPrice.isdigit():
         return JsonResponse({"status":"failure", "message":"Page, max price and min price must be number", "data":None})
      if int(maxPrice)<=int(minPrice):
         return JsonResponse({"status":"failure", "message":"max price can not be less than or equal to min price", "data":None})
      if not noOfProductPerPage:
         noOfProductPerPage=os.getenv("NO_OF_PRODUCT_PER_PAGE")
      if not noOfProductPerPage.isdigit():
         return JsonResponse({"status":"failure", "message":"No of product per page must be a number", "data":None})

      page=int(page)-1
      noOfProductPerPage=int(noOfProductPerPage)
      print(noOfProductPerPage)
      data=Product.objects.filter(Q(Q(description__contains=query) | 
      Q(name__contains=query)),Q(price__range=(minPrice,maxPrice)))
      tog=True
      noOfRows=len(data)
      
      if noOfRows!=0:
         tog=False
         noOfPage=noOfRows//noOfProductPerPage
         if noOfRows%noOfProductPerPage==0:
            noOfPage=(noOfRows//noOfProductPerPage)-1
         
         if page>noOfPage:
            page=noOfPage
         if page>noOfPage-1:
            tog=True

         data=data[page*noOfProductPerPage:page*noOfProductPerPage+noOfProductPerPage]
   
      data = json.loads(serializers.serialize('json', data))
      return JsonResponse({"status":"success", "message":"Data received", "data":data,"tog":tog})
   except:
      return JsonResponse({"status":"failure", "message":"An error occurred", "data":None})




def viewItem(request):
   try:
      if not request.POST:
         return JsonResponse({"status":"failure", "message":"Invalid request", "data":None})
      productId=request.POST.get('product_id')
      if not productId:
         return JsonResponse({"status":"failure", "message":"Product id required", "data":None})
      if not productId.isdigit():
         return JsonResponse({"status":"failure", "message":"Product id must be number", "data":None})
      data=Product.objects.filter(id=productId)
      data = json.loads(serializers.serialize('json', data))
      return JsonResponse({"status":"success", "message":"Data received", "data":data})
   except:
      return JsonResponse({"status":"failure", "message":"An error occurred", "data":None})



def createItem(request):
   try:
      if not request.POST:
         return JsonResponse({"status":"failure", "message":"Invalid request", "data":None})
      name=request.POST.get('name')
      description=request.POST.get('description')
      price=request.POST.get('price')
      availableQuantity=request.POST.get('available_quantity')
      if not name or not description or not price or not availableQuantity:
         return JsonResponse({"status":"failure", "message":"All fields are required", "data":None})
      if not isFloat(price):
         return JsonResponse({"status":"failure", "message":"Price must be integer or decimal", "data":None})
      if not availableQuantity.isdigit():
         return JsonResponse({"status":"failure", "message":"Available quantity must be an integer", "data":None})
      with transaction.atomic():
         productObj=Product(name=name,description=description,price=price,available_quantity=availableQuantity)
         productObj.save()

      return JsonResponse({"status":"success", "message":"Item created", "data":Product.objects.latest('id').id})

   except:
      return JsonResponse({"status":"failure", "message":"An error occurred", "data":None})




def editItem(request):
   try:
      if not request.POST:
         return JsonResponse({"status":"failure", "message":"Invalid request", "data":None})
      productId=request.POST.get('product_id')
      name=request.POST.get('name')
      description=request.POST.get('description')
      price=request.POST.get('price')
      availableQuantity=request.POST.get('available_quantity')
      if not productId or not name or not description or not price or not availableQuantity:
         return JsonResponse({"status":"failure", "message":"All fields are required", "data":None})
      if not isFloat(price):
         return JsonResponse({"status":"failure", "message":"Price must be integer or decimal", "data":None})
      if not availableQuantity.isdigit() or not productId.isdigit():
         return JsonResponse({"status":"failure", "message":"Available quantity and product id must be integer", "data":None})
      with transaction.atomic():
         Product.objects.filter(id=productId).update(name=name,description=description,price=price,available_quantity=availableQuantity)
      return JsonResponse({"status":"success", "message":"Item updated", "data":None})
   except:
      return JsonResponse({"status":"failure", "message":"An error occurred", "data":None})


def deleteItem(request):
   # try:
      if not request.POST:
         return JsonResponse({"status":"failure", "message":"Invalid request", "data":None})
      productId=request.POST.get('product_id')
      Product.objects.filter(pk=int(productId)).delete()
      return JsonResponse({"status":"success", "message":"Item deleted", "data":None})
   # except:
   #    return JsonResponse({"status":"failure", "message":"An error occurred", "data":None})


def createOrder(request):
   if not request.POST:
      return JsonResponse({"status":"failure","message":"Invalid request"})
   token=request.COOKIES.get('token')
   id=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"] 
   cartObj=Cart.objects.filter(customer_id=id)
   data=cartObj[0].product_list
   data=json.loads(data)
   productIdList=[]
   productQuantityList=[]
   total=0
   for i in data:
      productIdList.append(i['product_id'])
      productQuantityList.append(i['product_quantity'])
   productPriceList=Product.objects.values_list('price').filter(id__in=productIdList)
   for i in range(len(productPriceList)):
      total=total+productPriceList[i][0]*int(productQuantityList[i])
   current_date_time = datetime.now().replace(microsecond=0) 

   orderObj=Orders(customerid=User.objects.filter(id=id)[0],status='created',created_time=current_date_time,order_total=total)
   orderObj.save()
   orderId=Orders.objects.latest('id').id
   tblName="myapp_orderdetails"
   colList=["order_id","product_id","product_quantity","product_price"]
   valueList=[]
   for i in range(len(productPriceList)):
      valueList.append((orderId,int(productIdList[i]),int(productQuantityList[i]),float(str(productPriceList[i][0]))))
   with transaction.atomic():
      insert_into(tblName,colList,valueList)
   return JsonResponse({"status":"success", "message":"Order created", "data":None})





def addToCart(request):
   try:
      if not request.POST:
         return JsonResponse({"status":"failure", "message":"Invalid request", "data":None})
      productId=request.POST.get('product_id')
      productQuantity=request.POST.get('product_quantity')
      if not productId or not productQuantity:
         return JsonResponse({"status":"failure", "message":"All fields are required", "data":None})

      token=request.COOKIES.get('token')
      id=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"] 
      jsonData={"product_id":productId,"product_quantity":productQuantity}
      cartObj=Cart.objects.filter(customer_id=id)
      data=cartObj[0].product_list

      if data!="":
         data=json.loads(data)
         temp=True
         for i in data:
            if(i["product_id"]==productId):
               i["product_quantity"]=int(i["product_quantity"])+int(productQuantity)
               temp=False
         if temp:
            data.append(jsonData)
      else:
         data=[jsonData]
      data=json.dumps(data)

      cartObj.update(product_list=data)
      return JsonResponse({"status":"success", "message":"Added to cart", "data":None})
   except:
      return JsonResponse({"status":"failure", "message":"An error occurred", "data":None})


def removeFromCart(request):
      if not request.POST:
         return JsonResponse({"status":"failure", "message":"Invalid request", "data":None})
      token=request.COOKIES.get('token')
      id=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"] 
      productId=request.POST.get("product_id")
      if not productId:
         return JsonResponse({"status":"failure", "message":"Product id is required", "data":None})

      cartObj=Cart.objects.filter(customer_id=id)
      data=cartObj[0].product_list
      data=json.loads(data)
      for i in range(len(data)):
         if(data[i]['product_id'])==productId:
            data[i]="del"
      data.remove("del")
      data=json.dumps(data)
      cartObj.update(product_list=data)
      return JsonResponse({"status":"success", "message":"Removed from cart", "data":None})


def getCartdata(request):
   try:
      token=request.COOKIES.get('token')
      id=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"]
      result=0
      cartObj=Cart.objects.filter(customer_id=id)
      data=cartObj[0].product_list
      if data!="":
         data=json.loads(data)
         result=len(data)
      return JsonResponse({"status":"success", "message":"Data recieved", "data":{"no_of_item":result}})
      
   except:
      return JsonResponse({"status":"failure", "message":"An error occurred", "data":None})
  

def logout(request):
   if not request.method=="POST":
      return JsonResponse({"status":"failure", "message":"Invalid request", "data":None})
   response=JsonResponse({"status":"success", "message":"Cookie deleted", "data":None})
   response.delete_cookie('token')
   return response






def checkout(request):
   try:
      token=request.COOKIES.get('token')
      id=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"]
      cartObj=Cart.objects.filter(customer_id=id)
      data=cartObj[0].product_list
      if len(data)!=0:
         data=json.loads(data)
      productIdList=[]
      productIdQuantity=[]
      for i in data:
         productIdList.append(int(i['product_id']))
         productIdQuantity.append(int(i['product_quantity']))
      data=Product.objects.filter(id__in=productIdList)
      data = json.loads(serializers.serialize('json', data))
      total=0
      for i in range(len(productIdQuantity)):
         data[i]['fields']['quantity']=productIdQuantity[i]
         total=total+float(data[i]['fields']['price'])*int(productIdQuantity[i])
      return JsonResponse({"status":"success", "message":"Check out", "data":data,"total":total})
   except:
      return JsonResponse({"status":"failure", "message":"An error occurred", "data":None})

# def orderHistoryForAdmin(request):
   # try:
      # if not request.method=="POST":
      #    return JsonResponse({"status":"failure", "message":"Invalid request", "data":None})
      # page=request.POST.get('page')
      # if not page:
      #    return JsonResponse({"status":"failure", "message":"Page is required", "data":None})
      # data=OrderDetails.objects.select_related().annotate(
      #    name=F('product__name'),description=F('product__description')).values('id','order_id','product_quantity','product_price','name','description') 

      # data=list(data)
      
      # for i in data:
      #    i['product_price']=float(i['product_price'])
      # data=json.dumps(data)
      # data=json.loads(data)
      # return JsonResponse({"status":"success", "message":"Order history", "data":data})
   # except:
   #    return JsonResponse({"status":"failure", "message":"An error occurred", "data":None})

def orderHistoryForAdmin(request):
   if not request.method=="POST":
      return JsonResponse({"status":"failure", "message":"Invalid request", "data":None})
   token=request.COOKIES.get('token')
   id=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"] 
   print(id)
   page=request.POST.get('page')
   if not page:
      return JsonResponse({"status":"failure", "message":"Page is required", "data":None})
   data=OrderDetails.objects.select_related().annotate(
      name=F('product__name'),description=F('product__description')).annotate(customer_id=F('order__customerid'),time=F('order__created_time')).values('id','order_id','product_quantity','product_price','name','description','customer_id','time') 
   data=list(data)
   page=int(page)
   tog=False
   noOfRows=len(data)
   rem=noOfRows%10
   if rem==0:
      noOfPage=noOfRows//10
   else:
      noOfPage=noOfRows//10+1
   if page>noOfPage:
      page=noOfPage
   if page>noOfPage-1:
      tog=True

 

   data=data[(page-1)*10:page*10]
   for i in data:
      i["time"]=str(i["time"])[:-6]
   for i in data:
      i['product_price']=float(i['product_price'])
   data=json.dumps(data)
   data=json.loads(data)
   return JsonResponse({"status":"success", "message":"Order history", "data":data,"tog":tog})
def orderHistoryForUser(request):
   if not request.method=="POST":
      return JsonResponse({"status":"failure", "message":"Invalid request", "data":None})
   token=request.COOKIES.get('token')
   id=jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"] 
   print(id)
   page=request.POST.get('page')
   if not page:
      return JsonResponse({"status":"failure", "message":"Page is required", "data":None})
   data=OrderDetails.objects.select_related().annotate(
      name=F('product__name'),description=F('product__description')).annotate(customer_id=F('order__customerid'),time=F('order__created_time')).filter(customer_id=id).values('id','order_id','product_quantity','product_price','name','description','customer_id','time') 
   data=list(data)
   page=int(page)
   tog=False
   noOfRows=len(data)
   rem=noOfRows%10
   if rem==0:
      noOfPage=noOfRows//10
   else:
      noOfPage=noOfRows//10+1
   if page>noOfPage:
      page=noOfPage
   if page>noOfPage-1:
      tog=True

 

   data=data[(page-1)*10:page*10]
   for i in data:
      i["time"]=str(i["time"])[:-6]
   for i in data:
      i['product_price']=float(i['product_price'])
   data=json.dumps(data)
   data=json.loads(data)
   return JsonResponse({"status":"success", "message":"Order history", "data":data,"tog":tog})
   










   







      






         
  

 



