import datetime
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from manager.models import category, covertypetable, product
from users.models import cart, orderitems, ordertb
from django.contrib.auth.models import User


def adminhome(request):
    return render(request,'admin/adminhome.html')

def addcategory(request):
    return render(request,'admin/category_tb.html')

def categoryadd(request):
    if request.method == 'POST':
         p= request.POST['category']
         m=category.objects.create(name=p)
         m.save()
         messages.info(request,'category added')
    return render(request,'admin/addcategory.html')  
   
def viewdeatiles(request):
      m=category.objects.all()
      p={'m':m}
      return render(request,'admin/category_tb.html',p)

def edit(request):
     return render(request,'edit.html')

def update(request,id):
    m=get_object_or_404(category,id=id)
    if request.method == 'POST':
           categ=request.POST['category']
           m.name=categ
           m.save()
           messages.info(request,'updated')
           return redirect('viewdeatiles')
    m=category.objects.filter(id=id)
    p={'m':m}
    return render(request,'admin/edit.html',p)

def delete(request,id):
     u=category.objects.filter(id=id).delete()
     return redirect('viewdeatiles')


def covertypeadd(request):
    if request.method == 'POST':
         p= request.POST['covertype']
         n=covertypetable.objects.create(covertype=p)
         n.save()
         messages.info(request,'covertype added')
    return render(request,'admin/covertype_tb.html')  

def viewcovertype(request):
      n=covertypetable.objects.all()
      p={'n':n}
      return render(request,'admin/showcover.html',p)

def covertypeedit(request):
     return render(request,'covertypeedit.html')

def coveredit(request,id):
     n=get_object_or_404(covertypetable,id=id)
     if request.method == 'POST':
           cover=request.POST['covertype']
           n.covertype=cover
           n.save()
           messages.info(request,'updated')
           return redirect('viewcovertype')
     n=covertypetable.objects.filter(id=id)
     s={'n':n}
     return render(request,'admin/covertypeedit.html',s)

def deletecover(request,id):
     m=covertypetable.objects.filter(id=id).delete()
     return redirect('viewcovertype')

def productadd(request):
     if request.method =='POST':
         title=request.POST['title']
         ISBN=request.POST['ISBN']
         author=request.POST['author']
         description=request.POST['description']
         listprise=request.POST['listprice']
         price=request.POST['price']
         price50=request.POST['price50']
         price100=request.POST['price100']
         categorys=request.POST['category']
         covertype=request.POST['covertype']
         if len(request.FILES)>0:
              imge=request.FILES['image']
         else:
              imge='no image'    
         n=product.objects.create(title=title,ISBN=ISBN,author=author,description=description,listprise=listprise,price=price,price50=price50,price100=price100,categorys_id=categorys,covertype_id=covertype,image=imge)
         n.save()
         messages.info(request,'product added')
     cate=category.objects.all()
     cover=covertypetable.objects.all()
     return render(request,'admin/product_tb.html',{'ca':cate,'co':cover})   

def viewproduct(request):
      n=product.objects.all()
      p={'n':n}
      return render(request,'admin/productshow.html',p) 

def productedit(request,id):
     r=get_object_or_404(product,id=id)
     if request.method == 'POST':
         title=request.POST['title']
         ISBN=request.POST['ISBN']
         author=request.POST['author']
         description=request.POST['description']
         listprise=request.POST['listprice']
         price=request.POST['price']
         price50=request.POST['price50']
         price100=request.POST['price100']
         categorys=request.POST['category']
         covertype=request.POST['covertype']
         if len(request.FILES)>0:
              imge=request.FILES['image']
         else:
              imge='no image'    
         r.title=title 
         r.ISBN=ISBN
         r.author=author
         r.description=description
         r.listprise=listprise
         r.price=price
         r.price50=price50
         r.price100=price100
         r.categorys_id=categorys
         r.covertype_id=covertype
         r.image=imge
         r.save()
         messages.info(request,'updated')
         return redirect('viewproduct')
     cate=category.objects.all()
     cover=covertypetable.objects.all()
     n=product.objects.filter(id=id)
     return render(request,'admin/editproduct.html',{'ca':cate,'co':cover,'s':n})

def deleteproduct(request,id):
     m=product.objects.filter(id=id).delete()
     return redirect('viewproduct')

def logout(request):
     if request.user.is_authenticated:
           request.session.flush()
     return redirect('login')

def adminview(request):
      n=ordertb.objects.all()
      p={'n':n}
      return render(request,'admin/managerview.html',p) 

def deatilesshow(request,id):
    m=ordertb.objects.filter(id=id)
    n=orderitems.objects.filter(order_id=id)
    p={'m':m,'n':n}
    return render(request,'admin/showdusereatiles.html',p) 

def cancel(request,id):
     a=ordertb.objects.filter(id=id).update(orderstatus='Rejected')
     b={'a':a}
     return redirect('adminview')

def show(request):
     return render(request,'admin/showing.html')

def getid(request):
     numb=request.GET.get('type')
     if (numb == '1'):
         orders= ordertb.objects.filter(orderstatus='inprocess')
         p={'n':orders}
     elif (numb == '2'):
         orders= ordertb.objects.filter(orderstatus='pending') 
         p={'n':orders} 
     elif(numb == '3'):
         orders=ordertb.objects.filter(orderstatus='completed')
         p={'n':orders}  
     elif (numb == '4'):
          orders= ordertb.objects.filter(orderstatus='Rejected') 
          p={'n':orders}  
     elif(numb == '5'):
           orders= ordertb.objects.all() 
           p={'n':orders} 
     return render(request,'admin/managerview.html',p) 
def ordersts(request,id):
     a=ordertb.objects.filter(id=id).update(orderstatus='inprocess')
     b={'a':a}
     return redirect('adminview')

def shipordr(request):
    if request.method == 'POST':
         carrier=request.POST['carrier']
         tracking=request.POST['tracking']
         shippingdate=request.POST['shippingdate']
         id=request.POST['orderid']
         ordrtb=ordertb.objects.filter(id=id)
         ordrtb.update(carrier=carrier,tracking=tracking,shippingdate=shippingdate,orderstatus='completed')
    return redirect('adminview')

def search(request):
     prodct=request.GET.get('title')
     if prodct:
          n=product.objects.filter(title__icontains=prodct)
     else:
          n=product.objects.all()
     return render(request,'admin/productshow.html',{'n':n}) 

# def changepasword(request):
#      if request.method == 'POST':
#           old_password=request.POST['old_password']
#           new_password=request.POST['new_password']
#           confirm_password=request.POST['confirm_password']
#           if new_password == confirm_password:
#                data=User.objects.filter(password=old_password)
#                if data.count()>0:
#                     n=User.objects.filter(email=data[0].email).update(password=new_password)
#                     messages.info(request,'password updated')
#           else:
#              messages.info(request,'password incorrect')
#              return redirect('adminhome')
#      return render(request,'admin/changepassword.html')          

        


               



    
     

 



 






     












    





# Create your views here.


        



