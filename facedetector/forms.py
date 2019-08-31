from django import forms
from .models import *


class HotelForm(forms.ModelForm):
    ailments = forms.ModelMultipleChoiceField(queryset=Ailments.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Hotel
        fields = ['name', 'hotel_Main_Img','ailments','email']
    def __init__(self,*args,**kwargs):
        super(HotelForm,self).__init__(*args,**kwargs)
        self.fields['name'].widget.attrs.update({'class':'form-control'})
        self.fields['hotel_Main_Img'].widget.attrs.update({'class': 'form-control'})
        self.fields['ailments'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

class IndexForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['hotel_Main_Img']

