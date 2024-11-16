from django.urls import path
from users import views
from users.views import (
    
    CancelView,
    SuccessView,
    
)
urlpatterns=[
    path('',views.user_login,name="login"),
    path('login_user',views.login_user,name="login_user"),
    path('registration',views.registration,name="registration"),
    path('home',views.home,name="home"),
    path('viewdeatiles',views.viewdeatiles,name="viewdeatiles"),
    path('logoutuser',views.logoutuser,name="logoutuser"),
    path('deatiles/<int:id>',views.deatiles,name="deatiles"),
    path('addcart',views.addcart,name="addcart"),
    path('shopcart',views.shopcart,name="shopcart"),
    path('trash/<int:id>',views.trash,name="trash"),
    path('addproduct/<int:id>',views.addproduct,name="addproduct"),
    path('deleteproductlist/<int:id>',views.deleteproductlist,name="deleteproductlist"),
    path('summary',views.summary,name="summary"),
    # path('ordertable',views.ordertable,name="ordertable"),
    path('checkout',views.checkout,name="checkout"),
    path('cancel/',CancelView.as_view(),name="canel"),
    path('success/', SuccessView.as_view(), name='success'),
    path('checkout/<pk>/',views.checkout,name='checkout'),
    path('changepassword',views.changepassword,name="changepassword"),
    path('password_reset_request/', views.password_reset_request, name='password_reset_request'),
    path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    



]