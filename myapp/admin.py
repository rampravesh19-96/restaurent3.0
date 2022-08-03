from django.contrib import admin
from .models import User,Customer,OrderDetails,Orders,Product
# Register your models here.
 
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(OrderDetails)
admin.site.register(Orders)
admin.site.register(Product)

