from django.shortcuts import redirect, render
from .models import Users , Phone, Student, Collector,PhoneStatus
from django.contrib import messages
from .util import hash_password , check_password ,check_role_and_token_collector, check_role_and_token , check_valied_uuid , send_email_to_venue_owner , check_cookie , ActiveUser
from django.http import JsonResponse, HttpResponse , HttpResponseRedirect
from django.core import serializers
from .exception_handler import UnauthorizedUser
import uuid
import os
import asyncio
from django.http import HttpResponse
from threading import Thread
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Exists
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin
from .forms import AssignPhoneForm,PickupForm, DeliverForm,RepairForm,CollectForm, UpdateStatusForm
from django.db import connection
from django.db.models import Subquery, OuterRef



logged_user = None

def home(request):
   """Pending
   this metho will render index page (home view)
   """
   return render(request, 'public/home.html',{})
   #return render(request, 'public/home.html', {'venues': Venue.objects.all()[:8],'user_logged' : check_cookie(request),'hello':'hello world'})
     
def termsandconditions(request):
    return render(request,'public/termsandconditions.html')

def login(request):
   """
   this method will render login view
   """
   if check_cookie(request):
      if request.COOKIES.get("role")==3:
          return redirect('collector_dashboard')
      return redirect('dashboard')
   else:
   
      return render(request, 'public/login.html')

def signup(request):
   """
   this will render the signup view
   """
   return render(request, 'public/signup.html')

def logout(request):
   if request.method == 'POST':
      response = JsonResponse({'logout': True})
      response.delete_cookie('at')
      response.delete_cookie('user')
      return response
   else:
      return redirect('/')

def collector_dashboard(request):
    check_role_and_token_collector(3, request)
    global logged_user
    active_user = Collector.objects.get(id=request.COOKIES.get("user"))
   
    return render(request, 'public/collector/collector_dashboard.html',
           {'me': active_user ,
            'myphones':Phone.objects.filter(CollectorName = request.COOKIES.get("user")),
              'notifications':Phone.objects.filter(
                           Q(Collected = 'No')
                           & Q(CollectorName = request.COOKIES.get("user"))),
              #'students':Student.objects.filter(
                      #Q(school = request.COOKIES.get("school")))
              
                      'students':Student.objects.filter(
                             Exists(Phone.objects.filter(GRNumber=OuterRef('pk')))
                             & Q(school = request.COOKIES.get("school"))
                              )
            })






def dashboard(request):
   """
   this method will render dashboard
   """
   check_role_and_token(2, request)
   bookings = Bookings.objects.filter(owner_id=request.COOKIES.get("user"))
   booked_venues = Venue.objects.filter(owner_id=request.COOKIES.get("user"),booking=False)
   venues = Venue.objects.filter(owner_id=request.COOKIES.get("user"))
   pin = request.COOKIES.get("pin")
   maxpin = int(pin)+5
   minpin = int(pin)-5
   global logged_user
   active_user = Users.objects.get(id=request.COOKIES.get("user"))
   return render(request, 'public/dashboard/dashboard.html',
                 {'approved_bookings_list':Bookings.objects.filter(Q(status=True) & Q(owner_id=request.COOKIES.get("user")) & Q(from_date__gt=datetime.today().strftime("%Y-%m-%d"))),
                  'email_list':Bookings.objects.filter(Q(status=False) & Q(owner_id=request.COOKIES.get("user"))),
                  'bookings':len(bookings),'booked_venues':len(booked_venues),
                  'venues':len(venues) , 'me': active_user ,
                  'phones':Phone.objects.filter(
                        Q(Pincode__gte = minpin)
                        & Q(Pincode__lte = maxpin)
                          ),
                  'notifications':Phone.objects.filter(
                           Q(Pincode__gte = minpin)
                        & Q(Pincode__lte = maxpin)
                           & Q(CollectorName = None)),
                  'myphones':Phone.objects.filter(manager = request.COOKIES.get("user"))
                  })




def view_venue(request, venue_id):
   """
   this method will render venue details page
   """
   if check_valied_uuid(venue_id) :
      return render(request, 'public/venue.html', {'venue': get_object_or_404(Venue,id=venue_id) , 'user_logged' : check_cookie(request)})
   else:
        return redirect('/')

def collectors(request):

   """
   this method will render venue table to dashboard
   """
   check_role_and_token(2, request)
   global logged_user
   return render(request, 'public/dashboard/collectors.html', 
                 {'collectors': Collector.objects.filter(manager=request.COOKIES.get("user")) , 'me' : Users.objects.get(id=request.COOKIES.get("user")), 'notifications':Bookings.objects.filter(Q(status=False) & Q(owner_id=request.COOKIES.get("user")))})



def venues(request):

   """
   this method will render venue table to dashboard
   """
   check_role_and_token(2, request)
   global logged_user
   return render(request, 'public/dashboard/students.html', {'students': Student.objects.filter(manager=request.COOKIES.get("user")) , 'me' : Users.objects.get(id=request.COOKIES.get("user")), 'notifications':Bookings.objects.filter(Q(status=False) & Q(owner_id=request.COOKIES.get("user")))})

def add_collector(request):
   """
   this method will render add venue view
   """
   check_role_and_token(2, request)
   global logged_user
   return render(request, 'public/dashboard/add_collector.html',{'me': Users.objects.get(id=request.COOKIES.get("user")), 'notifications':Bookings.objects.filter(Q(status=False) & Q(owner_id=request.COOKIES.get("user")))})



   
def add_venue(request):
   """
   this method will render add venue view
   """
   check_role_and_token(2, request)
   global logged_user
   return render(request, 'public/dashboard/add_student.html',{'me': Users.objects.get(id=request.COOKIES.get("user")), 'notifications':Bookings.objects.filter(Q(status=False) & Q(owner_id=request.COOKIES.get("user")))})

def get_venues_by_category(request, category):
   """
   this method will render get venue by category view
   """
   return render(request, 'public/venues_by_category.html', {'venue_list_by_category': Venue.objects.filter(Q(category__contains=category.replace('&','')) | Q(name__contains=category.replace('&',''))) , 'user_logged' : check_cookie(request)})
def book_venue(request, venue_id):
   """
   this method will render book view
   """
   if check_valied_uuid(venue_id):
      return render(request, 'public/book.html', {'venue': get_object_or_404(Venue,id=venue_id) , 'user_logged' : check_cookie(request)})
   else:
      return redirect('/')
def emails(request):
   check_role_and_token(2, request)
   global logged_user
   return render(request,'public/dashboard/emails.html',{'email_list':Bookings.objects.filter(Q(status=False) & Q(owner_id=request.COOKIES.get("user"))),'me': Users.objects.get(id=request.COOKIES.get("user")) , 'notifications':Bookings.objects.filter(Q(status=False) & Q(owner_id=request.COOKIES.get("user")))})

def edit_profile(request):
   """
   this method will render edit profile view
   """
   check_role_and_token(2, request)
   global logged_user
   return render(request, 'public/dashboard/edit_profile.html', {'user': Users.objects.get(id=request.COOKIES.get("user")), 'me': Users.objects.get(id=request.COOKIES.get("user")), 'notifications':Bookings.objects.filter(Q(status=False) & Q(owner_id=request.COOKIES.get("user")))})

def venues_by_location(request, location):
   return render(request,'public/all_venues.html',{'venue_list': Venue.objects.filter(address=location),'user_logged': check_cookie(request)})

def all_venues(request):
   return render(request,'public/all_venues.html',{'venue_list': Venue.objects.all(),'user_logged': check_cookie(request)})

def edit_venue(request , venue_id):
   """
   this method will render edit menue view
   """
   check_role_and_token(2, request)
   if check_valied_uuid(venue_id) :
      venue = get_object_or_404(Venue,id=venue_id)
      if bool(venue):
         global logged_user
         return render(request, 'public/dashboard/edit_venue.html', {'venue': venue , 'me' : Users.objects.get(id=request.COOKIES.get("user")), 'notifications':Bookings.objects.filter(Q(status=False) and Q(owner_id=request.COOKIES.get("user")))})
      else:
         return redirect('/dashboard/students')
   else:
      return redirect('/dashboard/students')

def signup_user(request):
   """
   this method will register the user to system
   also checks the user email exists or not
   """
   if (request.method == 'POST'):
      if Users.objects.filter(email=request.POST.get('email')).exists():
         messages.info(request, 'This Email Already Exists')
         return redirect('/signup')
      else:
         Users(email=request.POST.get("email"), password=hash_password(request.POST.get("password")), 
               schoolname=request.POST.get('schoolname'), 
               schooladdress=request.POST.get('schooladdress'), 
               pincode=request.POST.get('pincode'), 
               udise=request.POST.get('udise'), 
               principal=request.POST.get('principal'), 
               phonenumber=request.POST.get("phonenumber")).save()
         messages.info(request, 'Thank You for Signing Up')
         return redirect('/signup')
   else:
      return redirect('/signup')

def booking_success(request, booking_id):
   """
   this method will render booking success view
   """
   if check_valied_uuid(booking_id):
      booking = get_object_or_404(Bookings ,id=booking_id)
      return render(request, 'public/booking_success.html', {'booking': booking, 'venue': Venue.objects.get(id=booking.venue_id), 'user_logged': check_cookie(request)})
     
   else:
      return redirect('/')

def get_user_by_email_address(request , email):
   """
   this method will return a json for ajax requests
   this method will available users with a email address
   """
   return JsonResponse(serializers.serialize('json', Users.objects.filter(email=email)), safe=False)
   
def venues_sort_by(request, sort_by):
   return render(request,'public/all_venues.html',{'venue_list': Venue.objects.all().order_by(sort_by),'user_logged': check_cookie(request)})


def user_login(request):
   """
   this method will accept POST request header and this method will login user 
   and issue a token cookie
   """
   if (request.method == 'POST'):
      global logged_user
      user = Users.objects.filter(email=request.POST.get("email")).first()
      collector = Collector.objects.filter(Email=request.POST.get("email")).first()
      if bool(user):
         if check_password(request.POST.get("password"), user.password):
            if(user.role == 1):
               response = HttpResponseRedirect('/admin/')
               response.set_cookie(key="at", value=user.role)
               response.set_cookie(key="user",value=user.id)
               response.set_cookie(key="school",value=user.schoolname)
               response.set_cookie(key="pin",value=user.pincode)
               return response
            else:
               #ActiveUser(first_name=user.first_name , avatar=user.avatar , id=user.id , last_name=user.last_name)
               # active_user = ActiveUser()
               # active_user.first_name = user.first_name
               # active_user.last_name = user.last_name
               # active_user.avatar = user.avatar
               response = HttpResponseRedirect('/dashboard/')
               response.set_cookie(key="at", value=user.role)
               response.set_cookie(key="user",value=user.id)
               response.set_cookie(key="school",value=user.schoolname)
               response.set_cookie(key="pin",value=user.pincode)
               return response
            """
            else:
               response = HttpResponseRedirect('/collector_dashboard/')
               response.set_cookie(key="at", value=user.role)
               response.set_cookie(key="user",value=user.id)
               response.set_cookie(key="school",value=user.school)
               response.set_cookie(key="pin",value=user.pincode)
               return response
           """
           
         else:
            raise UnauthorizedUser('Wrong Password')
      elif bool(collector):
         if check_password(request.POST.get("password"), collector.Password):
            if(collector.role == 3):
               response = HttpResponseRedirect('/collector_dashboard/')
               response.set_cookie(key="at", value=collector.role)
               response.set_cookie(key="user",value=collector.id)
               response.set_cookie(key="school",value=collector.school)
               response.set_cookie(key="pin",value=collector.Pincode)
               return response
         else:
            raise UnauthorizedUser('Wrong Password')
             
      else:
           raise UnauthorizedUser('Wrong Email Address')
   else:
        return redirect('/login')
          
            
            
"""   
            
        else:
            raise UnauthorizedUser('Wrong Password')
      else:
         raise UnauthorizedUser('Wrong Email Address')
   else:
      return redirect('/login')
"""

"""
def save_assign(request):
   check_role_and_token(2, request)
   phone = Phone.objects.get(id=request.POST.get("id"))
   if request.method == 'POST':
      #venue.address = request.POST.get("address")
      phone.Collectorassigned = request.POST.get("Collectorassigned")
      phone.ToStudent = request.POST.get("ToStudent")
      phone.save()
      return redirect('/dashboard')
   else:
      return redirect('/dashboard')

"""
def pickup(request,id):
    check_role_and_token_collector(3, request)
    template_name = 'public/collector/pickup.html'
    
    form = PickupForm(request.POST or None, instance = get_object_or_404(Phone,pk=id)) 
  
    context = {'phone':get_object_or_404(Phone,pk=id),'form':form}
  
    #template_name = 'public/dashboard/assign_phone.html'
    if form.is_valid():
        form.save()
        return redirect ('collector_dashboard')
    return render(request,template_name,context)
    
    """
    def form_valid(self,form):
        global cname
        instance = form.save(commit = False)
        cname = instance.CollectorName
        instance.save()
        return redirect ('collector_dashboard')
    """

def deliver(request,id):
    check_role_and_token_collector(3, request)
    template_name = 'public/collector/deliver.html'
    
    form = DeliverForm(request.POST or None, instance = get_object_or_404(Student,pk=id)) 
  
    context = {'student':get_object_or_404(Student,pk=id),'form':form}
  
    #template_name = 'public/dashboard/assign_phone.html'
    if form.is_valid():
        instance = form.save(commit = False)
        gr = instance.GRNumber
        vgr = instance.vGRNumber
        if gr == vgr :
            instance.hasphone = 'yes'
            instance.save()
            with connection.cursor() as cursor:
                cursor.execute("UPDATE collector SET hastask = hastask-1 WHERE id = %s", [request.COOKIES.get("user")])
            return redirect ('collector_dashboard')
        else: 
            return render(request,template_name,context)
    return render(request,template_name,context)
    
def collectrepair(request,id):
    check_role_and_token_collector(3, request)
    template_name = 'public/collector/collectrepair.html'
    
    form = CollectForm(request.POST or None, instance = get_object_or_404(Phone,pk=id)) 
  
    context = {'phone':get_object_or_404(Phone,pk=id),'form':form}
  
    #template_name = 'public/dashboard/assign_phone.html'
    if form.is_valid():
        instance = form.save(commit = False)
        
        instance.save()
        return redirect ('collector_dashboard')
    
    return render(request,template_name,context)
 
def updatestatus(request,id):
    check_role_and_token_collector(3, request)
    template_name = 'public/collector/updatestatus.html'
    
    form = UpdateStatusForm(request.POST or None, instance = get_object_or_404(Phone,pk=id)) 
  
    context = {'phone':get_object_or_404(Phone,pk=id),'form':form}
  
    #template_name = 'public/dashboard/assign_phone.html'
    if form.is_valid():
        instance = form.save(commit = False)
        instance.Delivered = 'yes'
        instance.save()
        return redirect ('collector_dashboard')
    
    return render(request,template_name,context)
    



def giverepair(request,id):
    check_role_and_token_collector(3, request)
    template_name = 'public/collector/giverepair.html'
    
    form = RepairForm(request.POST or None, instance = get_object_or_404(Phone,pk=id)) 
  
    context = {'phone':get_object_or_404(Phone,pk=id),'form':form}
  
    #template_name = 'public/dashboard/assign_phone.html'
    if form.is_valid():
        instance = form.save(commit = False)
        instance.AtService = 'Yes'
        instance.save()
        return redirect ('collector_dashboard')
    
    return render(request,template_name,context)
    


def save_assign(request,id):
    check_role_and_token(2, request)
    template_name = 'public/dashboard/assign_phone.html'
    
    form = AssignPhoneForm(request.POST or None, instance = get_object_or_404(Phone,pk=id)) 
  
    context = {'form':form}
  
    cname = ''
    def form_valid(self,form):
        global cname
        instance = form.save(commit = False)
        instance.manager = self.request.COOKIES.get("user")
        cname = instance.CollectorName
        with connection.cursor() as cursor:
            cursor.execute("UPDATE collector SET hastask = hastask + 1 WHERE CollectorName = %s", [cname])
        instance.save()
        return redirect ('dashboard')
    return render(request,template_name,context)



#in use
def save_collector(request):
   """
   this method will accept only POST request headers and it will save venues to the database
   """
   check_role_and_token(2, request)
   if request.method == 'POST':
      Collector(CollectorName=request.POST.get("CollectorName"),
              Email=request.POST.get("Email"), 
              Password=hash_password(request.POST.get("Password")), 
              CollectorAddress=request.POST.get("CollectorAddress"), 
              Pincode=request.POST.get("Pincode"), 
              PhoneNumber=request.POST.get("PhoneNumber"), 
              hastask = 0,
              school=request.COOKIES.get("school"),
              #img_two=request.FILES.get("image_two"), img_three=request.FILES.get("image_three"), price=request.POST.get("price"), category=request.POST.get("category"), address=request.POST.get("address"), 
              manager=request.COOKIES.get("user")).save()
      return redirect('/dashboard/collectors')
   else:
      return redirect('/dashboard/collectors')




#in use
def save_student(request):
   """
   this method will accept only POST request headers and it will save venues to the database
   """
   check_role_and_token(2, request)
   if request.method == 'POST':
      Student(firstname=request.POST.get("firstname"),
              lastname=request.POST.get("lastname"), 
              email=request.POST.get("email"), 
              GRNumber=request.POST.get("GRNumber"), 
              classname=request.POST.get("classname"), 
              rollnumber=request.POST.get("rollnumber"), 
              phonenumber = request.POST.get("phonenumber"), 
              address = request.POST.get("address"),
              pincode = request.POST.get("pincode"), 
              hasphone = 'No',
              school=request.COOKIES.get("school"),
              #img_two=request.FILES.get("image_two"), img_three=request.FILES.get("image_three"), price=request.POST.get("price"), category=request.POST.get("category"), address=request.POST.get("address"), 
              manager=request.COOKIES.get("user")).save()
      return redirect('/dashboard/students')
   else:
      return redirect('/dashboard/students')

def update_venue(request):
   """
   this metho will update the venue
   """
   check_role_and_token(2, request)
   venue = Venue.objects.get(id=request.POST.get("id"))
   if bool(venue) and request.method == 'POST':
      venue.address = request.POST.get("address")
      venue.description = request.POST.get("description")
      venue.name = request.POST.get("name")
      if request.FILES.get("image_one"):
         venue.img_one = request.FILES.get("image_one")
      else:
         venue.img_one = venue.img_one
      if request.FILES.get("image_two") :
         venue.img_two = request.FILES.get("image_two")
      else:
         venue.img_two = venue.img_two
      if request.FILES.get("image_three") :
         venue.img_three = request.FILES.get("image_three")
      else:
         venue.img_three = venue.img_three
      venue.price = request.POST.get("price")
      venue.category = request.POST.get("category")
      venue.save()
      return redirect('/dashboard/students')
   else:
      return redirect('/dashboard/students')

def delete_venue(request):
   """
   this metho will delete venue from database and removes all media files from the system
   """
   check_role_and_token(2, request)
   if request.method == 'POST':
      venue = Venue.objects.get(id=request.POST.get("id"));
      bookings = Bookings.objects.filter(venue_id=request.POST.get("id"))
      if bool(bookings):
         bookings.delete()
      
      path_list = []
      if(venue.img_one != ""):
         path_list.append(venue.img_one.path)
      if(venue.img_two != ""):
         path_list.append(venue.img_two.path)
      if(venue.img_three != ""):
         path_list.append(venue.img_three.path)
      for path in path_list:
         if os.path.isfile(path):
            os.remove(path)
      venue.delete()
      return JsonResponse({'delete':'deleted'})
   else:
      return redirect('/dashboard/students')

#in use
def success(request):
    context = {}
    return render(request,'success.html',context)

#in use
class GiftPhone(CreateView):
    model = Phone
    template_name = 'public/giftphone.html'
    fields = ['Name','Email','Address','Contact_Number','Pincode',
              'Phone_Company','Model_Name','Network','Camera','Phone_Rating',
              'Charger','Earphones','Requires_Repair']
    success_url = '/success'
    
    def form_valid(self,form):
        instance = form.save(commit = False)
        #instance.manager = self.request.user
        instance.AtService ='No'
        instance.RecievedService = 'No'
        instance.Collected = 'No'
        instance.Delivered = 'No'
        instance.CollectorName = None
        instance.GRNumber = None
        instance.manager = None
        instance.save()
        return redirect('home')

class AddStudent(LoginRequiredMixin,CreateView):
    model = Student
    template_name = 'public/dashboard/add_venue.html'
    #user = Users.objects.get(id=request.POST.get("id"))
    fields = ['firstname','lastname','email','gender','GRNumber','classname','rollnumber']
    success_url = '/success'
   
    def form_valid(self,form):
        
        instance = form.save(commit = False)
        instance.manager = self.request.user
        instance.save()
        return redirect('dashboard')

class AssignPhone(PassRequestMixin,  generic.CreateView):
    form_class = AssignPhoneForm
    template_name = 'public/dashboard/assign_phone.html'

def assignphone(request):
   check_role_and_token(2, request)
   global logged_user
   return render(request, 'public/dashboard/assign_phone.html',{'me': Users.objects.get(id=request.COOKIES.get("user")), 
                                                                'notifications':Bookings.objects.filter(Q(status=False) & Q(owner_id=request.COOKIES.get("user"))),
                                                                'collectors': Collector.objects.filter(manager=request.COOKIES.get("user")),
                                                                'students': Student.objects.filter(manager=request.COOKIES.get("user"))
                                                                
                                                                })



def put_phone_for_gift(request):
   """
   this method will save order and send email to venue owner
   """
   if request.method == 'POST':
      user = Users.objects.get(id=request.POST.get("owner_id"))
      # loop = asyncio.get_event_loop()
      # loop.run_until_complete(runner(request, user))
      send_email_to_venue_owner(
            user.email,
            request.POST.get("venue_name"),
            request.POST.get("from_date"),
            request.POST.get('from_time'),
            request.POST.get("to_time"),
            request.POST.get("email"),
            request.POST.get("phone_number"))
      booking_id = uuid.uuid4()
      Bookings(
         id=booking_id,
         email_address=request.POST.get("email"),
         telephone_number=request.POST.get("phone_number"),
         from_date=request.POST.get("from_date"),
         to_date=request.POST.get("to_date"),
         from_time=request.POST.get("from_time"),
         to_time=request.POST.get("to_time"),
         owner_id=request.POST.get("owner_id"),
         address=request.POST.get("address"),
         first_name=request.POST.get("first_name"),
         last_name=request.POST.get("last_name"),
         venue_id=request.POST.get("id")
      ).save()
      return redirect('/book/success/{}'.format(booking_id))
   else:
      return redirect('/')

def approve_booking(request):
   if request.method == 'POST':
      venue = Venue.objects.get(id=request.POST.get("venue_id"))
      if bool(venue):
         venue.img_one = venue.img_one
         venue.img_two = venue.img_two
         venue.img_three = venue.img_three
         venue.address = venue.address
         venue.description = venue.description
         venue.name = venue.name
         venue.price = venue.price
         venue.category = venue.category
         venue.booking = True
         venue.save()
         booking = Bookings.objects.get(id=request.POST.get("id"))
         booking.email_address=booking.email_address
         booking.telephone_number=booking.telephone_number
         booking.from_date=booking.from_date
         booking.to_date=booking.to_date
         booking.from_time=booking.from_time
         booking.to_time=booking.to_time
         booking.owner_id=booking.owner_id
         booking.address=booking.address
         booking.first_name=booking.first_name
         booking.last_name=booking.last_name
         booking.venue_id=booking.venue_id
         booking.status = True
         booking.save()
         return JsonResponse({'booking': True})
   else:
      return redirect('/')

def delete_booking(request):
   if request.method == 'POST':
      Bookings.objects.get(id=request.POST.get("id")).delete()
      return JsonResponse({'deleted': True})
   else:
      return redirect('/')

def update_user(request):
   """
   this method will update user details
   """
   check_role_and_token(2,request)
   if request.method == 'POST':
      user = Users.objects.get(id=request.POST.get("id"))
      if bool(user):
         if bool(request.POST.get("new_password")) :
            user.email = request.POST.get("email")
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.password = hash_password(request.POST.get("new_password"))
            user.role = user.role
            if request.FILES.get("new_avatar"):
               user.avatar = request.FILES.get("new_avatar")
            else:
               user.avatar = user.avatar
            user.save()
            return redirect('/dashboard/')
         else:
            user.email = request.POST.get("email")
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.password = user.password
            user.role = user.role
            if request.FILES.get("new_avatar"):
               user.avatar = request.FILES.get("new_avatar")
            else:
               user.avatar = user.avatar
            user.save()
            return redirect('/dashboard/')
      else:
         return redirect('/dashboard/')
   else:
      return redirect('/dashboard/')

def not_found_error(request , exception):
   return render(request, 'public/404_page.html',{'me': logged_user})
