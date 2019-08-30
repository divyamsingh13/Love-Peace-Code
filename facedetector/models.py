from django.db import models

# Create your models here.

class Ailments(models.Model):
    TYPES=(
        ("1","influenza"),
        ("2","pneumonia"),
        ("3","asthma"),
        ("4", "bronchitis"),
        ("5", "tb"),
    )
    disease=models.CharField(max_length=50,choices=TYPES,blank=True)
    def __str__(self):
        return self.get_disease_display()


class Hotel(models.Model):
    name = models.CharField(max_length=50,unique=True)
    hotel_Main_Img = models.ImageField(upload_to='images/')
    air_range=models.IntegerField(null=True)
    ailments=models.ManyToManyField(Ailments)
    attendance=models.BooleanField(default=False)
    email=models.EmailField(null=True)