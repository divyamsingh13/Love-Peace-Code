from django import forms
from .models import *


class HotelForm(forms.ModelForm):
    ailments = forms.ModelMultipleChoiceField(queryset=Ailments.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Hotel
        fields = ['name', 'hotel_Main_Img','air_range','ailments']

class IndexForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['hotel_Main_Img']

