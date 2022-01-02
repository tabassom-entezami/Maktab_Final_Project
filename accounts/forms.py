from django import forms 
from allauth.account.forms import SignupForm
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm,UserCreationForm 
from django.forms import fields 
from .models import * 
# class CostumRegisterForm(forms.ModelForm): 
#     email=forms.EmailField(required=True) 
#     class Meta: 
#         model=CustomUser 
#         fields=['email','password',] 
#         widgets = { 
#             'password': forms.PasswordInput(), 
#         }  
 
#     def save(self, commit=True): 
#         user = super().save(commit=False) 
#         user.set_password(self.cleaned_data["password"]) 
#         if commit: 
#             user.save() 
#         return user


class CostumRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
        widgets = { 
             'password': forms.PasswordInput(), 
                } 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password"]) 
        if commit:
            user.save()
        return user
