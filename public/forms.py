from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from .models import Phone,Collector,Student


from django import forms 
from .models import Phone 
  
  
# creating a form 
class PickupForm(forms.ModelForm): 
  
    # create meta class 
    class Meta: 
        # specify model to be used 
        model = Phone
  
        # specify fields to be used 
        fields = ['Collected']      
                
        

class AssignPhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['CollectorName','GRNumber']
   
       
        
class DeliverForm(forms.ModelForm): 
  
    # create meta class 
    class Meta: 
        # specify model to be used 
        model = Student
  
        # specify fields to be used 
        fields = ['vGRNumber']  
        
        
class RepairForm(forms.ModelForm): 
        # create meta class 
    class Meta: 
        # specify model to be used 
        model = Phone
  
        # specify fields to be used 
        fields = ['AtRepairCenter']  
        
class CollectForm(forms.ModelForm): 
        # create meta class 
    class Meta: 
        # specify model to be used 
        model = Phone
  
        # specify fields to be used 
        fields = ['ReceivedService']  
        
class UpdateStatusForm(forms.ModelForm): 
        # create meta class 
    class Meta: 
        # specify model to be used 
        model = Phone
  
        # specify fields to be used 
        fields = []  
        
       

        
       
        
        
"""        
from django import forms
from .models import Person, City

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'birthdate', 'country', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()
"""