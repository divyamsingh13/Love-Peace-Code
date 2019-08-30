from django.db import models

# Create your models here.

class Ailments(models.Model):
    TYPES=(
        ("1","cancer"),
        ("2","tb"),
        ("3","hayabusa"),
    )
    disease=models.CharField(max_length=50,choices=TYPES,blank=True)


class Hotel(models.Model):
    name = models.CharField(max_length=50,unique=True)
    hotel_Main_Img = models.ImageField(upload_to='images/')
    air_range=models.IntegerField(null=True)
    ailments=models.ManyToManyField(Ailments)
