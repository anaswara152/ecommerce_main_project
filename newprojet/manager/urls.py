from django.urls import path
from manager import views
urlpatterns=[
    path('adminhome',views.adminhome,name='adminhome'),
    path('addcategory',views.addcategory,name="addcategory"),
    path('categoryadd',views.categoryadd,name="categoryadd"),
    path('viewdeatiles',views.viewdeatiles,name='viewdeatiles'),
    path('update/<int:id>',views.update,name="update"),
    path('dlete/<int:id>',views.delete,name="delete"),
    path('covertypeadd',views.covertypeadd,name="covertypeadd"),
    path('viewcovertype',views.viewcovertype,name="viewcovertype"),
    path('coveredit/<int:id>',views.coveredit,name="coveredit"),
    path('deletecover/<int:id>',views.deletecover,name="deletecover"),
    path('viewproduct',views.viewproduct,name="viewproduct"),
    path('productadd',views.productadd,name="productadd"),
    path('productedit/<int:id>',views.productedit,name="productedit"),
    path('deleteproduct/<int:id>',views.deleteproduct,name="deleteproduct"),
    path('logout',views.logout,name="logout"),
    path('adminview',views.adminview,name="adminview"),
    path('deatilesshow/<int:id>',views.deatilesshow,name="deatilesshow"),
    path('cancel/<int:id>',views.cancel,name="cancel"),
    path('show',views.show,name="show"),
    path('getid',views.getid,name="getid"),
    path('ordersts/<int:id>',views.ordersts,name="ordersts"),
    path('shipordr',views.shipordr,name="shipordr"),
    path('search',views.search,name="search"),
    # path('changepasword',views.changepasword,name="changepasword")
    
 ]

    # path('addsummary',views.addsummary,name="addsummary")






   
    
    

