from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Show(models.Model):
	title = models.CharField( max_length=100)
	poster = models.ImageField(upload_to="media/img")
	video =  models.FileField(upload_to= "media/video")
	Description = models.TextField()
	date= models.DateTimeField()
	tickets_no = models.IntegerField()
	def __str__(self):
		return self.title

class Admin:
	pass

class profile(models.Model):
	seller = models.ForeignKey(User)
	event = models.ForeignKey(Show, default = "0")
	
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
	amount = models.IntegerField()
	event = models.ForeignKey(Show)
	tike_type = models.CharField(max_length = 30)

	def __str__(self):
		return self.tike_type

class Admin:
	pass

class ticket(models.Model):
	phone_number = models.IntegerField(null = True)
	email = models.EmailField()
	Name = models.CharField(max_length = 100, default="0")
	pin = models.CharField(max_length = 10)
	event = models.ForeignKey(Show, null = True)
	seller = models.ForeignKey(profile, default ="0", null = True)
	ticket_type = models.ForeignKey(tickettype, default = "0", null = True)
	status = models.BooleanField(default = False)

	def __str__(self):
		return self.Name

class Admin:
	pass
