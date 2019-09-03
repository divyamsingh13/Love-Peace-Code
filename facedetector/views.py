import re

from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.utils.baseconv import base64
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from pip._vendor import requests

from .forms import *
from .function import *


# Create your views here.
API_URL="http://localhost:5000/predict"
@csrf_exempt
def index(request):
    if request.method=='POST':

        form=IndexForm(request.POST)
        print(form)
        print(form.errors)
        if form.is_valid():
            # name_received, accuracy = scriptToBeCalled(form.cleaned_data.get("hotel_Main_Img"))
            print("valid")
            print(form.cleaned_data['hotel_Main_Img'])
            image=form.cleaned_data['hotel_Main_Img']
            payload={"image":image}
            request1=requests.post(API_URL,files=payload).json()
            print(request1)
            name_received=""
            accuracy=0
            if(request1):
                name_received=request1["label"]
                accuracy=request1["probability"]

            # predict(form.cleaned_data['hotel_Main_Img'])
            print("name",name_received,accuracy)

            if(not(name_received=="")):
                hotel = Hotel.objects.filter(name=name_received)
                print(hotel)
                hotel = hotel[0]
                if(hotel.attendance==1):
                    message="Attendance already marked"
                else:
                    hotel.attendance=True
                    message="Attendance marked"
                    hotel.save()
                noOfDiseases = len(hotel.ailments.all())
                diseases=[]
                for i in hotel.ailments.all():
                    diseases.append(i.get_disease_display())
                print("no",noOfDiseases)
                return render(request, 'success.html', {"message": message,"noOfDiseases":noOfDiseases,"diseases":diseases})
            else:
                return render(request, 'unsuccess.html')
    else:
        form=IndexForm()
    return render(request, 'index1.html',{'form':form})




def hotel_image_view(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            hotel=form.save()
            noOfDiseases = len(hotel.ailments.all())
            disease = noOfDiseases
            air_index = 200
            if (noOfDiseases == 0):
                air_index = 200
            elif (noOfDiseases == 1):
                air_index = 175
            elif (noOfDiseases == 2):
                air_index = 150
            elif (noOfDiseases == 3):
                air_index = 125
            elif (noOfDiseases == 4):
                air_index = 100
            elif (noOfDiseases == 5):
                air_index = 75
            hotel.air_range=air_index
            print(form.cleaned_data.get('name'),form.cleaned_data.get('hotel_Main_Img'))
            hotel.save()
            name=hotel.name

            # if(accuracy>.80):
            #     return redirect('success')
            # else:
            #     return redirect("hotel_image_view")
            return render(request, 'image.html', {'form':name})

    else:
        form = HotelForm()
    return render(request, 'image_upload.html', {'form': form})


def success(request):
    return HttpResponse('successfuly uploaded')


def display_hotel_images(request):
    if request.method == 'GET':
        # getting all the objects of hotel.
        Hotels = Hotel.objects.all()
        return render(request=request, template_name='display_hotel_images.html',context={'hotel_images': Hotels})