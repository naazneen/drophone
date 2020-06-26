import bcrypt
from .exception_handler import UnauthorizedUser
import uuid
from django.conf import settings
from django.core.mail import send_mail
import asyncio
from threading import Thread
from .models import Users,Collector


def hash_password(password_text):
    """
    this method will generate bcrypt hash
    """
    return bcrypt.hashpw(password_text.encode('utf8'), bcrypt.gensalt(12)).decode('utf8')

def check_password(password, hashed_password):
    """
    this method is check passwords
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def check_role_and_token_collector(role, request):
    """
    this method will check the role and if role not eaqual it will raise a excepton
    """
    print('length',len(Collector.objects.filter(id=request.COOKIES.get("user"))))
    if check_vailed_integer(request.COOKIES.get("at")): 
        if bool(request.COOKIES.get("at")) and isinstance(request.COOKIES.get("at"),str):
            if role != int(request.COOKIES.get("at")) or len(Collector.objects.filter(id=request.COOKIES.get("user"))) != 1:
                raise UnauthorizedUser('Unauthroized User')
        else:
            raise UnauthorizedUser('Unauthroized User')
    else:
        raise UnauthorizedUser('Unauthroized User')




def check_role_and_token(role, request):
    """
    this method will check the role and if role not eaqual it will raise a excepton
    """
    print('length',len(Users.objects.filter(id=request.COOKIES.get("user"))))
    if check_vailed_integer(request.COOKIES.get("at")): 
        if bool(request.COOKIES.get("at")) and isinstance(request.COOKIES.get("at"),str):
            if role != int(request.COOKIES.get("at")) or len(Users.objects.filter(id=request.COOKIES.get("user"))) != 1:
                raise UnauthorizedUser('Unauthroized User')
        else:
            raise UnauthorizedUser('Unauthroized User')
    else:
        raise UnauthorizedUser('Unauthroized User')

def check_valied_uuid(uuid_str):
    """
    check string is an uuid or not if valied return true else return false
    """
    try:
        uuid_object = uuid.UUID(uuid_str, version=4)
    except ValueError:
        return False
    return str(uuid_object) == uuid_str

def send_email_to_venue_owner(to_email, venue_name, date, start_time, end_time, email, contact_no):
    return send_mail("Venue Booking", "There is a booking for your {} on : {} at : {} to : {}. Please send confirmation mail to {} contact no {}".format(venue_name, date, start_time, end_time, email, contact_no), settings.EMAIL_HOST_USER, [to_email], fail_silently=True)

def check_cookie(request):
    if check_vailed_integer(request.COOKIES.get("at")):
        if request.COOKIES.get("at") == '2' and bool(request.COOKIES.get("user")):
            return True
        else:
            return False
    else:
        return False

def check_vailed_integer(integer_val):
    try:
        if integer_val != None :
            int(integer_val)
            return True
        else:
            return False
    except ValueError:
        return False



class ActiveUser():

    first_name: str
    id: str
    avatar : object
    last_name: str

    # def __init__(self, *args, **kwargs):
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.avatar = avatar
    #     self.id = id
    
    # def __init__(self,first_name=None , avatar=None , id=None ,last_name=None ):
    #     self.first_name = first_name
    #     self.id = id
    #     self.avatar = avatar
    #     self.last_name = last_name
