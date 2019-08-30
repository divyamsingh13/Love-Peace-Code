from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *


# Create your views here.
def index(request):
    if request.method=='POST':
        form=HotelForm(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            # name_received, accuracy = scriptToBeCalled(form.cleaned_data.get("hotel_Main_Img"))
            print("valid")
            name_received="a"
            hotel=Hotel.objects.filter(name=name_received)
            return HttpResponse(hotel[0].name)
    else:
        form=HotelForm()
    return render(request, 'index.html', {'form': form})




def hotel_image_view(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            print(form.cleaned_data.get('name'),form.cleaned_data.get('hotel_Main_Img'))

            # if(accuracy>.80):
            #     return redirect('success')
            # else:
            #     return redirect("hotel_image_view")
            return HttpResponse("hello")

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