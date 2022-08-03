from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=500)
    is_admin = models.IntegerField(default=0)
    password_reset_otp=models.CharField(max_length=6) 
    password_reset_otp_time = models.DateTimeField(blank=True, null=True)
class Customer(models.Model):
    idd=models.ForeignKey(User, models.DO_NOTHING, db_column='idd')
    phone = models.CharField(max_length=10)
    dob = models.DateField()
    address = models.CharField(max_length=500)

class Orders(models.Model):
    customerid = models.ForeignKey(User, models.DO_NOTHING, db_column='customerId') 
    order_total = models.DecimalField(max_digits=9, decimal_places=2)
    status = models.CharField(max_length=100)
    created_time = models.DateTimeField()
    paid_time = models.DateTimeField(blank=True, null=True)
    cancel_time = models.DateTimeField(blank=True, null=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    available_quantity = models.IntegerField()

class OrderDetails(models.Model):
    order = models.ForeignKey(Orders,models.DO_NOTHING)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    product_quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=9, decimal_places=2)

class Cart(models.Model):
    customer = models.ForeignKey(User,models.DO_NOTHING)
    product_list = models.TextField()


