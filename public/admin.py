from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.
from .models import Users,Phone,Student,Collector,RepairCenter
from import_export.admin import ImportExportModelAdmin


admin.site.unregister(Group)

class UsersAdmin(ImportExportModelAdmin):
    model = Users
    list_display_links = ('schoolname',)
    list_display = ('schoolname','schooladdress','pincode','udise','principal',
                    'email','password','phonenumber')
    #list_editable = ('email',)
    list_filter = ('schoolname','schooladdress','pincode','udise','principal',
                    'email','password','phonenumber')
    search_fields = ('schoolname','schooladdress','pincode','udise','principal',
                    'email','password','phonenumber')
    
    
class PhoneAdmin(ImportExportModelAdmin):
    model = Phone
    list_display_links = ('Name',)
    list_display = ('Name','Email','Address','Contact_Number','Pincode',
              'Phone_Company','Model_Name','Network','Camera','Phone_Rating',
              'Charger','Earphones','Requires_Repair','CollectorName','GRNumber','manager',
              'Collected','Delivered','AtService','ReceivedService')
    list_filter = ('Name','Email','Address','Contact_Number','Pincode',
              'Phone_Company','Model_Name','Network','Camera','Phone_Rating',
              'Charger','Earphones','Requires_Repair')
    search_fields = ('Name','Email','Address','Contact_Number','Pincode',
              'Phone_Company','Model_Name','Network','Camera','Phone_Rating',
              'Charger','Earphones','Requires_Repair')
    
    
class StudentAdmin(ImportExportModelAdmin):
    model = Student
    list_display_links = ('firstname','lastname',)
    list_display = ('school','firstname','lastname','email','address','pincode','phonenumber','GRNumber',
                    'classname','rollnumber','hasphone',)
    list_filter = ('school','firstname','lastname','email','address','pincode','phonenumber','GRNumber',
                    'classname','rollnumber','hasphone',)
    search_fields = ('school','firstname','lastname','email','address','pincode','phonenumber','GRNumber',
                    'classname','rollnumber','hasphone',)
    
    
    
class CollectorAdmin(ImportExportModelAdmin):
    model = Collector
    list_display_links = ('CollectorName',)
    list_display = ('CollectorName','Email','Password','CollectorAddress','Pincode',
                    'PhoneNumber','hastask','school','role',)
    list_filter = ('CollectorName','Email','Password','CollectorAddress','Pincode',
                    'PhoneNumber','hastask','school','role',)
    search_fields = ('CollectorName','Email','Password','CollectorAddress','Pincode',
                    'PhoneNumber','hastask','school','role',)
    
    
    
class RepairAdmin(ImportExportModelAdmin):
    model = RepairCenter
    list_display_links = ('Name',)
    list_display = ('Name','Address','Pincode','PhoneNumber',)
    list_filter = ('Name','Address','Pincode','PhoneNumber',)
    search_fields = ('Name','Address','Pincode','PhoneNumber',)
    
admin.site.register(Users,UsersAdmin)
admin.site.register(Phone,PhoneAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Collector,CollectorAdmin)
admin.site.register(RepairCenter,RepairAdmin)