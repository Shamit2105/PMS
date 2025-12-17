from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from base.models import BaseModel
from misc.models import Address

class UserProfile(BaseModel):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='profiles')
    first_name = models.CharField()
    last_name = models.CharField()
    dob = models.DateField()
    contact_number = models.CharField()
    address = models.ForeignKey(to=Address,on_delete=models.SET_NULL,related_name='user',null=True,blank=True)
    class Meta:
        db_table = 'User_Profiles'

        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

        

