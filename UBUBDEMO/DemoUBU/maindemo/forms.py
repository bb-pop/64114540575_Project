from django import forms

from maindemo.models import Item, UserProfile


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'