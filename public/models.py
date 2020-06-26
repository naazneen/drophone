from django.db import models
import uuid
import os
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.timezone import datetime
# Create your models here.

class Users(models.Model):
    #id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    role = models.SmallIntegerField(default=2)
    avatar = models.ImageField(upload_to='pro_pics')
    ###mychange
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    SchoolName = models.CharField(max_length=30,name = "schoolname")
    SchoolAddress = models.CharField(max_length=80,name = "schooladdress")
    Pincode = models.IntegerField(name = "pincode")
    UDISE = models.CharField(max_length = 50,name = "udise")
    Principal = models.CharField(max_length=50,name = "principal")
    Email = models.EmailField(max_length=40, name = "email")
    Password = models.TextField(max_length=40,name = "password")
    PhoneNumber = models.CharField(max_length = 10,name = "phonenumber")
    class Meta:
        db_table = 'Users'
        
#class Collectors(models.model):
    
       
    
    
    

@receiver(models.signals.pre_save, sender=Users)
def auto_del_when_avatar_update(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(id=instance.id).avatar
    except sender.DoesNotExist:
        return False

    new_files = instance.avatar
    
    # if not old_file == new_file or old_file_two == instance.img_two or old_file_three == instance.img_three:
    #     for old_file_in_list in old_files_list:
    #         if os.path.isfile(old_file_in_list.path):
    #             os.remove(old_file_in_list.path)
    if not new_files == old_file:
        if bool(old_file) :
            if os.path.exists(old_file.path):
                os.remove(old_file.path)


    
###my models
    

# Create your models here.

# Create your models here.

#---Phone status from Donor to Student repair center

class Student(models.Model):
    #id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    #manager = models.ForeignKey(Users,on_delete = models.CASCADE,default = None)
    manager = models.UUIDField()
    firstname = models.CharField(max_length = 30)
    lastname = models.CharField(max_length = 30)
    email = models.EmailField(default = None)
    address = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    phonenumber = models.CharField(max_length = 10)
    #gender = models.CharField(max_length = 20,choices = (('male','MALE'),('female','FEMALE'),('other','OTHER')))
    #date_added = models.DateTimeField(default = datetime.now())
    GRNumber = models.CharField(max_length = 10)
    classname = models.CharField(max_length = 30)
    rollnumber = models.CharField(max_length = 10)
    hasphone = models.CharField(max_length=10,default = "No")
    school = models.CharField(max_length = 50)
    vGRNumber = models.CharField(max_length = 10,default = None,null = True)
    class Meta:
        db_table = 'Student'
    def __str__(self):
        return self.GRNumber


class Collector(models.Model):
    #id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    manager = models.UUIDField()
    role = models.SmallIntegerField(default=3)
    #SchoolName = models.ForeignKey(Users,on_delete = models.CASCADE,default = None,max_length=30)
    CollectorName = models.CharField(max_length=60)
    Email = models.EmailField(max_length=250) 
    Password = models.CharField(max_length=100)
    CollectorAddress = models.CharField(max_length=50)
    Pincode = models.IntegerField()
    PhoneNumber = models.CharField(max_length=10)
    #hastask = models.CharField(max_length = 5,default = 'No')
    hastask = models.IntegerField()
    school = models.CharField(max_length = 50)
    class Meta:
        db_table = 'Collector'
    def __str__(self):
        return self.CollectorName

class RepairCenter(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    Name =  models.CharField(max_length=200)
    Address = models.CharField(max_length=200)
    Pincode = models.IntegerField()
    PhoneNumber = models.CharField(max_length = 10)
    class Meta:
        db_table= 'Reapir_Center'
    def __str__(self):
        return (self.Name+","+self.Address)
    



class Phone(models.Model):
    #id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    Name = models.CharField(max_length=50)
    Email = models.EmailField(max_length=30,)
    Address = models.CharField(max_length=50)
    Pincode = models.IntegerField()
    Contact_Number = models.CharField(max_length = 10)
    Phone_Company = models.CharField(max_length=50,)
    Model_Name = models.CharField(max_length=50)
    r1='1'
    r2='2'
    r3='3'
    r4='4'
    r5='5'
    r6='6'
    r7='7'
    r8='8'
    r9='9'
    r10='10'
    rChoices=((r1,'1'),(r2,'2'),(r3,'3'),(r4,'4'),(r5,'5'),(r6,'6'),(r7,'7'),(r8,'8'),
    (r8,'8'),(r9,'9'),(r10,'10'))
    Net='3G'
    high='4G'
    YChoices=((Net,'3G'),
              (high,'4G'))
    Network = models.CharField(max_length=2, choices=YChoices,default =0)          
    Camera1 = 'FrontCamera'
    Camera2 = 'BackCamera'
    Camera3 = 'Front and back'
    Camera4 = 'With Out Camera'
    camerachoices=((Camera1,'FrontCamera'),
                   (Camera2,'BackCamera'),
                   (Camera3,'Front and back'),
                   (Camera4,'With Out Camera'))
    Camera = models.CharField(max_length=15,choices=camerachoices,default=0)


    Phone_Rating = models.CharField(max_length=50,choices=rChoices,default=0)
    yescharger = 'Yes'
    nocharger  = 'No'
    cCharger= ((yescharger,'Yes'),(nocharger,'No'))
    Charger = models.CharField(max_length=25,choices=cCharger,default=0)
    yesearphone = 'Yes'
    noearphone  = 'No'
    cErphone= ((yesearphone,'Yes'),(noearphone,'No'))
    Earphones = models.CharField(max_length=30,choices=cErphone,default=0)
    use = 'Yes'
    nonuse = 'No'
    cUse = ((nonuse,'No'),(use,'Yes'))
    Requires_Repair= models.CharField(max_length=40,choices=cUse,default=1)
    #picked = models.CharField(max_length=50,choices = (('yes','yes'),('no','no')),default = None,null = True)
    AtService = models.CharField(max_length=50,choices = (('yes','yes'),('no','no')),default = None,null = True)
    ReceivedService = models.CharField(max_length=50,choices = (('yes','yes'),('no','no')),default = None,null = True)
    Collected = models.CharField(max_length=50,choices = (('yes','yes'),('no','no')),default = 'No',null = True)
    Delivered = models.CharField(max_length=30,choices = (('yes','yes'),('no','no')),default = None,null = True)
    #ThePhone = models.ForeignKey(Phone,on_delete = models.CASCADE,default = None,max_length=30)
    #ToStudent = models.CharField(max_length=200,default = None,null = True)
    AtRepairCenter = models.ForeignKey(RepairCenter,null = True,default=None,on_delete = models.SET_NULL)
    #Collectorassigned = models.CharField(max_length=200,default = None,null = True)
    CollectorName = models.ForeignKey(Collector,null = True,default=1,on_delete = models.SET_NULL)
    GRNumber = models.OneToOneField(Student,null = True,default=None,on_delete = models.SET_NULL)
    manager = models.UUIDField(null = True)
    class Meta:
        db_table = 'Phone'




class PhoneStatus(models.Model):
    id = models.ForeignKey(Phone,primary_key = True,on_delete = models.CASCADE)
    AtService = models.CharField(max_length=50,choices = (('yes','yes'),('no','no')))
    ReceivedService = models.CharField(max_length=50,choices = (('yes','yes'),('no','no')))
    Collected = models.CharField(max_length=50,choices = (('yes','yes'),('no','no')))
    Delivered = models.CharField(max_length=30,choices = (('yes','yes'),('no','no')))
    #ThePhone = models.ForeignKey(Phone,on_delete = models.CASCADE,default = None,max_length=30)
    #ToStudent = models.ForeignKey(Student,null = True,on_delete = models.CASCADE,default = None,max_length=30)
    AtRepairCenter = models.ForeignKey(RepairCenter,null = True,on_delete = models.CASCADE,default = None,max_length=30)
    #CollectorAssigned = models.ForeignKey(Collector,on_delete = models.CASCADE,default = None,max_length=30)
    CollectorName = models.ForeignKey(Collector,null = True,default=1,on_delete = models.SET_NULL)
    GRNumber = models.ForeignKey(Student,null = True,default=1,on_delete = models.SET_NULL)
    
    
    class Meta:
        db_table = 'Phone_status'




#--making choices for #G and 5G

"""
Added
class School(models.Model):
    Id = models.AutoField(primary_key=True)
    SchoolName = models.CharField(max_length=30,name = "School Name")
    SchoolAddress = models.CharField(max_length=80,name = "School Address")
    Pincode = models.IntegerField(name = "PinCode")
    UDISE = models.CharField(max_length = 50,name = "UDISE Number")
    Principal = models.CharField(max_length=50,name = "Principal Name")
    Email = models.EmailField(max_length=40, name = "Email")
    Password = models.CharField(max_length=40,name = "Password")
    PhoneNumber = models.IntegerField(name = "Phone Number")
    class Meta:
        db_table = 'School'
"""
