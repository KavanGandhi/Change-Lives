from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from change_lives_app1.models import Signup,Contact,Registration,Payment_model,Patient_Model
from django.conf import settings
import stripe
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail

# Create your views here.
def index(request):
    return render(request,'index.html')
def aboutt(request):
    return render(request,'about.html')

def contactt(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        subject=request.POST.get('sub')
        text=request.POST.get('textarea')
        
        contact=Contact(name=name,email=email,ph_no=phone,subject=subject,message=text)
        contact.save()

        if contact is not None:
            messages.success(request,"your data has been saved securly")
            return redirect('index')
        
    return render(request,'contact.html')

def loginn(request):
    if request.method=='POST':
        user=request.POST.get('user_login')
        password=request.POST.get('password_login')
        user =authenticate(username=user
                           ,password=password)
        
        if user is not None:
            login(request,user)
            return render(request,'success.html')
        else:
            return redirect('about')
    return render(request,'index.html')
        
def logoutt(request):
    logout(request)
    return redirect('index')

def ngo_login(request):
    if request.method=='POST':
        user=request.POST.get('ngo_user')
        password=request.POST.get('ngo_password')
        user =authenticate(username=user
                           ,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('patient')
        else:
            return redirect('404')
    return render(request,'login_of_ngo.html')

def signupp(request):
    if request.method=='POST':
        user=request.POST.get('userr')
        email=request.POST.get('emaill')
        password=request.POST.get('password')
        
        # signupp=Signup(user=user,email=email,password=password)\
        myuser=User.objects.create(username=user,email=email)
        myuser.set_password(password)
        
        if myuser is not None:
            login(request,myuser)
        # signupp.save()
            myuser.save()
        messages.success(request,"your data has been saved")
    return render(request,'index.html')

def success(request):
    data=Registration.objects.all()
    context={
        'data':data,
    }
    return render(request,'success.html',context)   
        
    
# old payment method


# def payment(request):
#     stripe.api_key=settings.STRIPE_PRIVATE_KEY
#     session=stripe.checkout.Session.create(payment_method_types=['card'],
#             line_items=[{
#                 'price':'price_1Mn3zNSB9lTxkE9Qe0S0uTun',
#                 'quantity':1,
#             }],
#             mode='payment',
#             success_url=request.build_absolute_uri(reverse('contact')),
#             cancel_url=request.build_absolute_uri(reverse('index')),)
#     context={
#         'session_id':session.id,
#         'stripe_public_key':settings.STRIPE_PUBLIC_KEY
#         }
#     return render(request,'payment.html',context)


def registrationn(request):
    if request.method=="POST":
        name=request.POST.get('name')
        registration_no=request.POST.get('registration_no')
        phone_no=request.POST.get('phone_no')
        state=request.POST.get('state')
        upload_file=request.POST.get('photo')
        email=request.POST.get('email_regist')
        password=request.POST.get('password_regist')
        author_name=request.POST.get('author_name')
        print(upload_file)
        
        
        ngo_user=User.objects.create(username=name,email=email)
        ngo_user.set_password(password)
        
        registration=Registration(name=name,registration_no=registration_no,phone_no=phone_no,state=state,document=upload_file,email=email,password=password,author_name=author_name)
        
        
        if ngo_user is not None:
            login(request,ngo_user)

            registration.save()
            ngo_user.save()
        
        if registration is not None:
            messages.success(request,'Your registration is succefully completed!!')
            return redirect('patient')
        else:
            return render(request,'index.html')
        
    return render(request,'registration.html')
    
    

def payment(request):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY

    if request.method == "POST":
        amount = int(request.POST["amount_pay"]) 
        #Create customer
        amount_payment=request.POST.get('amount_pay')
        email_payment=request.POST.get('email')
        full_name_payment=request.POST.get('full_name')
            
        if amount>int(999999):
            return HttpResponse("please enter the amount less than 999999.99")
            
        paymentt_gateway=Payment_model(amount=amount_payment,email=email_payment,name=full_name_payment)
            
        try:
            customer = stripe.Customer.create(
                email=request.POST.get("email"),
                name=request.POST.get("full_name"),
                description="Test donation",
                source=request.POST['stripeToken']
            )

        except stripe.error.CardError as e:
            return HttpResponse("<h1>There was an error charging your card:</h1>"+str(e))     

        except stripe.error.RateLimitError as e:
            # handle this e, which could be stripe related, or more generic
            return HttpResponse("<h1>Rate error!</h1>")

        except stripe.error.InvalidRequestError as e:
            return HttpResponse("<h1>Invalid requestor!</h1>")

        except stripe.error.AuthenticationError as e:  
            return HttpResponse("<h1>Invalid API auth!</h1>")

        except stripe.error.StripeError as e:  
            return HttpResponse("<h1>Stripe error!</h1>")

        except Exception as e:  
            pass  

        #Stripe charge 
        charge = stripe.PaymentIntent.create(
            customer=customer,
            amount=int(amount)*100,
            currency='inr',
            description="Test donation"
        ) 
        transRetrive = stripe.PaymentIntent.retrieve(
            charge["id"],
            api_key="sk_test_51Mn3vTSB9lTxkE9QXNVfmKrpK2Biav5SxinzixgQOgxXjkODLvjCYBiCkhJctdE0G6i3HTU0rPqzcan1GtJiQOUx001bFFtbDl"
        )
        charge.save() # Uses the same API Key.
        paymentt_gateway.save()

        # Send email
        subject = 'Payment confirmation'
        message = f'Thank you for your payment of {amount} INR.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email_payment, 'ayushjluhar@gmail.com']
        send_mail(subject, message, from_email,recipient_list )

        return redirect("success")

    return render(request, "p.html")



def fundraiser(request):
    fundraiser_data=Patient_Model.objects.all()

    
    # payment=list(Payment_model.objects.all())
    patient_to_payment={}
    
    # for patientname in Patient_Model.objects.all():
    #     patient_to_payment[patientname.name]=sum([a.amount for a in list(Payment_model.objects.all().filter(name=patientname.name))])
    # return render(request,"fundraiser.html",{'payments':patient_to_payment})

    for patientname in Patient_Model.objects.all():
        payments = [(a.image, a.amount_pat, a.message) for a in Patient_Model.objects.filter(name=patientname.name)]
        total_amount = sum([a.amount for a in Payment_model.objects.filter(name=patientname.name)])
        # if total_amount>patientname.amount_pat:
        #     total_amount=total_amount-patientname.amount_pat
        #     return redirect('404')
        # else:
        patient_to_payment[patientname.name] = {'payments': payments, 'total_amount': total_amount}
    return render(request, "fundraiser.html", {'payments': patient_to_payment})


def patien(request):
    if request.method=='POST':
        name=request.POST.get('name')
        image=request.POST.get('image')
        amount_to_be_raised=request.POST.get('amount')
        message=request.POST.get('message')

        patientt=Patient_Model(name=name,image=image,amount_pat=amount_to_be_raised,message=message)
        
        patientt.save()
        
        if patientt is not None:
            return render(request,'index.html')
        else:
            return render(request,'404.html')
        
    return render(request,'patient.html')


def error404(request):
    return render(request,'404.html')