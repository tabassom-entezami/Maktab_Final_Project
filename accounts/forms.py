from django import forms
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
# from allauth.account.forms import SignupForm
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm,UserCreationForm 
from django.forms import fields
from django.contrib.auth.hashers import make_password
from resturant.models import Branch 
from .models import * 
class CostumRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    city = forms.CharField(max_length=20,required=True)
    street = forms.CharField(max_length=20,required=True)
    plaque = forms.IntegerField(min_value=1,required=True)
    class Meta:
        model = Customer
        fields = ( "username","email", "city","street","plaque","password1", "password2",)
        widgets = { 
             'password': forms.PasswordInput(), 
                } 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # user.city = self.cleaned_data['city']
        # user.street = self.cleaned_data['street']
        # user.plaque = self.cleaned_data['plaque']
        # user.set_password(self.cleaned_data["password"]) 
        if commit:
            user.save()
        return user



class CostumRegisterForm1(forms.ModelForm):
    
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,widget=forms.PasswordInput())
    password2 = forms.CharField(required=True,widget=forms.PasswordInput())
    # address = forms.CharField(required=True)
    # discreption = forms.TimeInput()
    
    class Meta:
        model = Branch
        fields = ("email","username","name", "address", "city", "discreption","is_open","category_id","password","password2",)
        
        widgets = { 
             'password': forms.PasswordInput(), 
             'password2': forms.PasswordInput(),
              
                } 
    def save(self, commit=True):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        password = make_password(self.cleaned_data['password'])
        manager = Manager.objects.create(username = username, password = password,email  = email)
        manager.save()
        name = self.cleaned_data["name"]
        category_id = self.cleaned_data['category_id']
        address = self.cleaned_data['address']
        city = self.cleaned_data['city']
        discreption = self.cleaned_data['discreption']
        is_open = self.cleaned_data['is_open']
        branch = Branch.objects.create(name = name,manager_id = manager , category_id =category_id ,address = address,city = city ,discreption = discreption, is_open =is_open )
        branch.save()

        

    # def clean_password2(self):
    #     super(CostumRegisterForm1, self).clean() 
    #     pas1 = self.cleaned_data.get('password')
    #     pas2 = self.cleaned_data.get("password2")
    #     if pas1 != pas2 and pas1 and pas2:
    #         self._errors['password'] = self.error_class([
    #             'not ok'])



#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
       
       
        # user.set_password(self.cleaned_data["password"]) 
        # if commit:
        #     user.save()
        # return user




class Address(forms.Form):
    city = forms.CharField(max_length=150,label="city" , required=True)
    street = forms.CharField(max_length=150,label="street",required=True)
    plaque = forms.IntegerField( label= "plaque",required=True,validators=[MinValueValidator(1)])

    


 