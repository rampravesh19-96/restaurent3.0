from django.urls import path,re_path
from . import api,views
 
 
urlpatterns = [
   path('api/register', api.register),
   path('api/login', api.login),
   path('api/forgot_password', api.forgotPassword),
   path('api/save_password', api.savePassword),
   path('api/edit_user_profile', api.editUserProfile),
   path('api/view_item_list', api.viewItemList),
   path('api/view_item', api.viewItem),
   path('api/create_item', api.createItem),
   path('api/edit_item', api.editItem),
   path('api/delete_item', api.deleteItem),
   path('api/create_order', api.createOrder),
   path('api/checkout', api.checkout),
   path('api/add_to_cart', api.addToCart),
   path('api/get_cart_data', api.getCartdata),
   path('api/remove_from_cart', api.removeFromCart),
   path('api/logout', api.logout),
   path('api/order_history_for_user', api.orderHistoryForUser),
   path('api/order_history_for_admin', api.orderHistoryForAdmin),

   path('register', views.register),
   path('login', views.login),
   path('forgot-password', views.forgotPassword),
   re_path(r'^save-password/$', views.savePassword),
   re_path(r'^viewitem/$', views.viewItem),
   path('', views.home),
   path('checkout', views.checkout),
   path('orderhistory', views.orderHistoryForUser),
   path('admin/orderhistory', views.orderHistoryAdmin),
   path('edituserprofile', views.editUserProfile),
   path('admin', views.admin),
   # path('viewitem/<productId>', views.viewItem),


]
