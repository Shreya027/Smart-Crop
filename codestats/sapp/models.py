from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms.models import model_to_dict
# Create your models here.


class MyUser(AbstractUser):
    mobile_no = models.CharField(max_length=10, unique=True)
    user_type = models.NullBooleanField(null=True)
    aadhar = models.CharField(max_length=20, null=True, blank=True)
    crops_subscribed_to = models.CharField(max_length = 100)             #dict of the format crop:start_date


class State_translator(models.Model):
    state_name = models.CharField(max_length=50, default=None)
    state_language = models.CharField(max_length=50, default=None)
    state_code = models.CharField(max_length=20, default="en")

    def __str__(self):
        return self.state_name

    def to_dict(self):
        return model_to_dict(self)



class Support(models.Model):
    user = models.ForeignKey("MyUser")
    support_text = models.TextField()
    is_read = models.BooleanField()


#class Recommendation(models.Model):                               #to calculate and store 
    # rainfall = models.CharField(max_length=30)                    #recommendations so that 
    # soil = models.CharField(max_length=30)                        #in the future it will be 
    # humidity = models.CharField(max_length=30)                    #faster for the same parameters 
    # temperature = models.CharField(max_length=30)
    # fertilizer = models.CharField(max_length=30)
    # crop = models.CharField(max_length=30)

    #replace all that with a foreign key to the area record and another to the crop

class Crop(models.Model):
    name = models.CharField(max_length = 100, primary_key = True)
    area = models.CharField(max_length = 100)
    soil_profile = models.CharField(max_length=100)
    water_req = models.CharField(max_length=50)
    temp_req = models.CharField(max_length=50)

class Area_Data(models.Model):
    area_num = models.IntegerField(primary_key = True)
    district = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    air_quality = models.CharField(max_length = 1000)             #retreived from API
    water_quality = models.CharField(max_length = 1000)           #csv
    soil_profile = models.CharField(max_length = 1000)            #csv
    temperature = models.CharField(max_length = 1000)             #not sure
    vegetation_index = models.CharField(max_length = 100)         #retreived from API
    crop_prices = models.CharField(max_length = 100)             #dict of crop:price (area specific prices) from API


class Crop_Alerts(models.Model):
    crop_name = models.CharField(max_length = 100)
    alert = models.CharField(max_length = 100)
    days = models.IntegerField()
