from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from . import models as mds

User = get_user_model()

@receiver(post_save,sender = User)
def create_profile(sender,instance,created,**kwargs):
    print("SIGNAL RUNNING")
    if created and instance.is_staff == True:
        queryset = mds.AdminUserProfile.objects.filter(user = instance)
        print(queryset)
        if not queryset.exists():
            mds.AdminUserProfile.objects.create(user = instance)
        else:
            instance.admin_user_profile.save()  
    elif created and instance.is_staff == False:
        queryset = mds.CustomerUserProfile.objects.filter(user = instance) 
        if not queryset.exists():          
            mds.CustomerUserProfile.objects.create(user = instance)
        else:
            instance.customer_user_profile.save()

          
""" @receiver(post_save,sender = User)
def save_profile(sender,instance,**kwargs):
    if instance.is_staff == True:
        
        instance.admin_user_profile.save()    
    elif instance.is_staff == False:
        if mds.CustomerUserProfile.objects.filter(user = instance) is not None:
            instance.customer_user_profile.save() """