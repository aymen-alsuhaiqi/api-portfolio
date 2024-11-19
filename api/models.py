from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserInformation(models.Model):
    user_id = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    job = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    summary = models.CharField(max_length=250)
    age = models.IntegerField()
    country = models.CharField(max_length=25)
    freelancer = models.BooleanField(default=False)
    image = models.ImageField(upload_to='user/profile/',blank=True,null=True)
    banner = models.ImageField(upload_to='user/banner/',blank=True,null=True)

    def __str__(self):
        return self.full_name
    
class Skill(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=50)
    skill_level = models.CharField(max_length=50)
    
    def __str__(self):
        return self.skill_name
    
class Education(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=100)
    degree = models.CharField(max_length=50)
    period = models.CharField(max_length=50)
    details = models.CharField(max_length=50)

    def __str__(self):
        return self.school_name
    
class Experience(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    job_description = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    period = models.CharField(max_length=50)
    details = models.CharField(max_length=250,blank=True)

    def __str__(self):
        return self.company_name
    
class Works(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    technical = models.CharField(max_length=50)
    image_project = models.ImageField(upload_to='projects/%Y/%m/%d',blank=True,null=True)

    def __str__(self):
        return self.title
