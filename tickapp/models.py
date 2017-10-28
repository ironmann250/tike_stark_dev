from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import datetime

# Create your models here.

class Show(models.Model):
    #idshow = models.CharField(max_length=10,primary_key=True) #why did you do this ;(
    title = models.CharField(max_length=100)
    Description = models.TextField(null=True,default='')
    date = models.DateTimeField()
    venue = models.CharField(max_length=100, default="0")
    tickets_no = models.IntegerField()
    supervisor=models.ForeignKey(User,default='0')

    def __str__(self):
        return self.title


class Admin:
    pass


class profile(models.Model):
    seller = models.ForeignKey(User)
    #iduser = models.CharField(primary_key=True, max_length = 40) #again seriously i wonder what's beneath
    event = models.ForeignKey(Show, default="0")
    def __str__(self):
        return self.seller.username


''' @receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
	'''


class Admin:
    pass


class tickettype(models.Model):
    tike_type = models.CharField(max_length=100)
    event = models.ForeignKey(Show)
    amount = models.IntegerField()
    #idticktype = models.CharField(primary_key=True,max_length =30) #this is just poor codes

    def __str__(self):
        return self.tike_type


class Admin:
    pass


class ticket(models.Model):
    event = models.CharField(max_length=100, null=True)
    phone_number = models.BigIntegerField(null=True)
    pin = models.CharField(max_length=10)
    email = models.EmailField(null=True)
    seller = models.CharField(max_length=20, null=True)
    Name = models.CharField(max_length=100)
    ticket_type = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)
    date=models.DateTimeField(default=timezone.now())#i hear there is a timezone module go ahead and use it instead
    def __str__(self):
        return self.Name
    


class Admin:
    pass
