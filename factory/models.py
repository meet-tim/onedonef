from django.db import models
import datetime



class District(models.Model):
    region = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Factory(models.Model):
    CATEGORY = (
        ('Agric','Agric'),
        ('Tech','Tech'),
        )

    CONDITION = (
            ('Green','Green'),
            ('Brown','Brown'),
            ('Completed','Completed'),
        )
    name =  models.CharField(max_length=100)
    district = models.OneToOneField(
        District,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    location = models.name = models.CharField(max_length=100)
    lat = models.FloatField(max_length=100)
    lon = models.FloatField(max_length=100)
    about = models.CharField(max_length=100)
    raw_materials = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    date_built = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    condition = models.CharField(max_length=100,choices=CONDITION)
    category = models.CharField(max_length=100,choices=CATEGORY)

    

    class Meta:
        ordering=['-date_built',]

    def __str__(self):
        return self.name

