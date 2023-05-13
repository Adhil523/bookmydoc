from django.db import models
import datetime

# Create your models here.
class Clinic(models.Model):
    cname=models.CharField(max_length=100)
    loc=models.CharField(max_length=50)
    landmark=models.CharField(max_length=50)
    dis=models.CharField(max_length=50)
    workhour_b=models.CharField(max_length=50)
    workhour_a=models.CharField(max_length=50)
    def __str__(self):
        return self.cname
    
class Bookings(models.Model):
    pname=models.CharField(max_length=100)
    cname=models.CharField(max_length=100)
    slot=models.CharField(max_length=10)
    d=models.DateField(default=datetime.datetime(2018,5,3))
    def __str__(self):
        return self.pname

