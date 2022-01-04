from .models import *
from django import forms

class FoodForm(forms.ModelForm):
    
    def init(self, *args, **kwargs):
        super(FoodForm, self).init(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Food
        exclude = ['food_created_date']

class FoodCategoryForm(forms.ModelForm):
    def init(self, *args, **kwargs):
        super(FoodCategoryForm, self).init(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Category
        fields = ("__all__")

class MealCategoryForm(forms.ModelForm):
    def init(self, *args, **kwargs):
        super(MealCategoryForm, self).init(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Meal
        fields = ("__all__")