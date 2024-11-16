import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
import stripe
from manager.models import product
from users.models import cart, orderitems, ordertb, register
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,get_user_model
from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator,default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator









# Create your views here.

def registration(request):
    if request.method == 'POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        # phone=request.POST['phone']
        email=request.POST['email']
        address=request.POST['address']
        city=request.POST['city']
        postalcode=request.POST['postalcode']
        state=request.POST['state']
        password=request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.info(request,'email existing')
            return render(request,'common/register.html')
        elif User.objects.filter(username=email).exists():
             messages.info(request,'email not existing')
             return render(request,'common/register.html')
        else:
            user=User.objects.create_user(username=username, first_name= first_name,last_name=last_name,email=email,password=password)
            user.save()
            customer=register(user=user,address=address,city=city,state=state,postalcode=postalcode)
            customer.save()
            customer_obj,create=Group.objects.get_or_create(name="CUSTOMER")
            customer_obj.user_set.add(user)

            return render(request,'common/login.html')

    return render(request,'common/register.html')


def user_login(request):
    return render (request,'common/login.html')     

def login_user(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name="CUSTOMER").exists():
            return redirect('home')
        else:
            return redirect('adminhome')
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user= authenticate(request,username=email,password=password)
        if user is not None:
            if user.groups.filter(name="CUSTOMER").exists():
                login(request,user)
                #request.session['username']=email

                return redirect(home)
            else:
                return redirect('adminhome')
        else:
            messages.error(request,'user credential is not correct')
            return render (request,'common/login.html')
def home(request):
    m=product.objects.all()
    p={'m':m}
    return render(request,'customer/home.html',p)

def viewdeatiles(request):
    return render(request,'admin/productshow.html')

def deatiles(request,id):
    m=product.objects.filter(id=id)
    p={'m':m}
    return render(request,'customer/showdeatiles.html',p) 
def addcart(request):
    if request.user.is_authenticated:
        id=request.POST['productid']
        productid=product.objects.get(id=id)
        print(productid.id)
        customerid=request.user.id
        print(customerid)
        count=int(request.POST['count'])
        print(count)
        if count<50:
            price=productid.price
            print(price)
        elif count<100:
            price=productid.price50
            print(price)
        else:
            price=productid.price100
            print(price)
     
        n=cart(customerid_id=customerid,productid_id=productid.id,count=count,price=price)
        n.save()
    return redirect(home)

def shopcart(request):
    id=request.user.id
    cart_obj=cart.objects.filter(customerid_id=id)
    grand=0
    for c in cart_obj:
        total=(c.count)*(c.price)
        grand=grand+total
    p={'n':cart_obj,'gr':grand}
    return render(request,'customer/shoppingcart.html',p)

def trash(request,id):
    productid=cart.objects.filter(id=id)
    customerid=request.user.id
    number=productid[0].count
    if number==0:
        messages.info('blank')
        return redirect('shopcart')
    else:
        quantity=number-1
        p=productid.update(count=quantity)
        return redirect('shopcart')
    
def addproduct(request,id):
    productid=cart.objects.filter(id=id)
    customerid=request.user.id
    num=productid[0].count
    if num==0:
        messages.info(request,'blank')
        return redirect('shopcart')
    else:
        qunt=num+1
        k=productid.update(count=qunt)
        return redirect(shopcart)
    
def deleteproductlist(request,id):
    m=cart.objects.filter(id=id).delete()
    return redirect('shopcart')    

def summary(request):
    id=request.user.id
    carttb=cart.objects.filter(customerid_id=id)
    cid=carttb[0].customerid
    v=register.objects.filter(user_id=cid)
    grand=0
    for c in carttb:
        total=(c.count)*(c.price)
        grand=grand+total
    p={'v':v ,'n':carttb,'gr':grand}
    return render(request,'customer/summary.html',p)

# def ordertable(request):
#     if request.method == 'POST':
#         name=request.POST['name']
#         phone=request.POST['phone']
#         address=request.POST['address']
#         city=request.POST['city']
#         state=request.POST['state']
#         email=request.POST['email']
#         orderdate=datetime.datetime.now()
#         id=request.user.id
#         ordertotal=request.POST['grandtotal']  
#         ordr=ordertb.objects.create(name=name,phone=phone,address=address,city=city,state=state,email=email,orderdate=orderdate,ordertotal=ordertotal,customerid_id=id)
#         ordr.save()
#         cid=request.user.id
#         cartta=cart.objects.filter(customerid_id=cid)
#         for k in cartta:
#             total=k.price
#             count=k.count
#             productid=k.productid.id
#             order=ordr.id      
#             item=orderitems(total=total,count=count,productid_id=productid,order_id=order)
#             item.save()
#         messages.info(request,'order confirmed')
        #   return redirect('shopcart')


    
def checkout(request):
    if request.method == "POST":
        name=request.POST['name']
        phone=request.POST['phone']
        address=request.POST['address']
        city=request.POST['city']
        state=request.POST['state']
        email=request.POST['email']
        orderdate=datetime.datetime.now()
        id=request.user.id
        ordertotal=request.POST['grandtotal']  
        ordr=ordertb.objects.create(name=name,phone=phone,address=address,city=city,state=state,email=email,orderdate=orderdate,ordertotal=ordertotal,customerid_id=id)
        ordr.save()
        cid=request.user.id
        cartta=cart.objects.filter(customerid_id=cid)
        for k in cartta:
            total=k.price
            count=k.count
            productid=k.productid.id
            order=ordr.id      
            item=orderitems(total=total,count=count,productid_id=productid,order_id=order)
            item.save()
            messages.info(request,'order confirmed')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        else:
            domain = request.build_absolute_uri('/')  # For production

        user_id = request.user.id
        products = cart.objects.filter(customerid_id=user_id)

        if not products.exists():
            return render(request, 'empty_cart.html')  # Handle empty cart case

        line_items = []
        for item in products:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.productid.title,
                        'description': item.productid.description,
                    },
                    'unit_amount': int(item.productid.price * 100),  # Convert dollars to cents
                },
                'quantity': item.count,
            })

        # Create the Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=domain + '/success/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain + '/cancel/',
            metadata={'orderid':ordr.id}

        )

        return redirect(checkout_session.url, code=303)

  

class SuccessView(TemplateView):
    template_name = "sucess.html"
    def get(self,request,*args,**kwargs):
        session_id=request.GET.get('session_id')
        if not session_id:
            return HttpResponse('session id is missing',status=400)
        try:
             session=stripe.checkout.Session.retrieve(session_id)
             print(session)
             if session.payment_status =="paid":
                 order_id=session.metadata.get('orderid')
                 order=get_object_or_404(ordertb,id=order_id)
                 order.paymentstatus="paid"
                 order.transactionid=session_id
                 order.paymentdate=datetime.datetime.now()
                 order.save()
        except stripe.error.StripeError as e:
           return HttpResponse(f"Stripe error: {str(e)}", status=500)         
        return super().get(request,*args,**kwargs)


class CancelView(TemplateView):
   template_name="cancel.html"

#  def checkoutviews(request):
#         id=request.user.id
#         products= cart.objects.filter(id=id)
# def get(request):
#         id=request.objects.id
#         products = cart.objects.filter(id=id)
#         return render(request, 'checkout.html', {'products': products})

# def post(request):
#     id=request.user.id
#     products = cart.objects.get(id=id)
#     checkout_session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=[{
#             'price_data': {
#                 'currency': 'usd',
#                 'product_data': {
#                     'name': products.productid.title,
#                     'description': product.description,
#                     },
#                     'unit_amount': int(products.price * 100),  # Stripe expects the amount in cents
#                 },
#                 'quantity': products.count,
#             }],
#             mode='payment',
#             success_url='request.build_absolute_uri'('/success/'),
#             cancel_url='request.build_absolute_uri'('/cancel/'),
#         )
#     return redirect(checkout_session.url, code=303)

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


def changepassword(request):
    if request.method == 'POST':
        old_password=request.POST['old_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']
        user=request.user
        if not user.check_password(old_password):
            messages.info(request,"the old password is correct")
        else:
            user.set_password(new_password)
            user.save() 
    return render(request,'customer/changepassword.html')           


# def forgotpassword(request):
#      if request.method =='POST':
#          email=request.POST['email']

def generate_token():
     return get_random_string(20)

def password_reset_request(request):
    if request.method == "POST":
         email = request.POST.get('email')
         try:
             user = User.objects.get(email=email)
         except User.DoesNotExist:
             messages.error(request, "User with this email does not exist.")
             return redirect('password_reset_request')

         token =default_token_generator.make_token(user)
         uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
         reset_url = request.build_absolute_uri(reverse('password_reset_confirm',kwargs={'uidb64':uidb64,'token':token}))
         subject = "Password Reset Request"
         message = render_to_string('customer/password_reset_email.html', {
             'user': user,
             'reset_url': reset_url,
         })
         send_mail(subject, message,settings.DEFAULT_FROM_EMAIL, [user.email])
         messages.success(request, "A password reset link has been sent to your email.")
         return render(request,'customer/password_reset_email.html')
        #  return render(request,'customer/password_reset_email.html')
    return render(request,'common/password_reset_form.html')
def password_reset_confirm(request, uidb64, token):
        User=get_user_model()
        try:
          uid = force_str(urlsafe_base64_decode(uidb64))
          user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            print(user)
        if user is not None and default_token_generator.check_token(user,token):
             if request.method == 'POST':
                  password1=request.POST.get('password1')
                  password2=request.POST.get('password2')

                  if password1 == password2:
                      user.password = make_password(password1)
                      user.save()
                    #   update_session_auth_hash(request,user)
                      messages.success(request,'your password has been reset')
                      return render(request,'customer/password_reset_confirm.html')
                  else:
                      messages.error(request,'password do not match')
                      return render(request,'common/password_reset_form.html')
                          
             return render(request,'customer/password_reset_confirm.html')
        else:
           return render(request,'common/password_reset_form.html')



        # return render(request, 'customer/password_reset_confirm.html')          
        # else:
        #      messages.error(request,'the password reset link is invalid') 
        #      return render(request,'customer/password_reset_confirm.html')
        # return HttpResponse("An unexpected error occurred.")       


# def password_reset_confirm(request, uidb64, token):
#     try:
        
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     token_generator = PasswordResetTokenGenerator()
#     if user is not None and token_generator.check_token(user, token):
#         if request.method == "POST":
#             password1 = request.POST.get('password1')
#             password2 = request.POST.get('password2')

#             if password1 == password2:
#                 user.password = make_password(password1)
#                 user.save()
#                 messages.success(request, "Your password has been reset. You can now log in.")
#                 return redirect('login')
#             else:
#                 messages.error(request, "Passwords do not match.")

#         return render(request, 'password_reset_confirm.html', {'validlink': True})
    
#     # messages.error(request, "The password reset link is invalid or has expired.")
#     return redirect('password_reset_request')


   
        












def logoutuser(request):
     if request.user.is_authenticated:
           request.session.flush()
     return redirect('login')