from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserInformation(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name_ar = models.CharField(max_length=100)  
    full_name_en = models.CharField(max_length=100)  
    address_ar = models.CharField(max_length=200)  
    address_en = models.CharField(max_length=200)  
    job_ar = models.CharField(max_length=30)  
    job_en = models.CharField(max_length=30)  
    phone_number = models.CharField(max_length=15)
    summary_ar = models.CharField(max_length=250)  
    summary_en = models.CharField(max_length=250)  
    age = models.IntegerField()
    country_ar = models.CharField(max_length=25)  
    country_en = models.CharField(max_length=25)  
    freelancer = models.BooleanField(default=False)
    image = models.ImageField(upload_to='user/profile/', blank=True, null=True)
    banner = models.ImageField(upload_to='user/banner/', blank=True, null=True)

    def __str__(self):
        return self.full_name_ar

class Skill(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_name_ar = models.CharField(max_length=50)  
    skill_name_en = models.CharField(max_length=50)  
    skill_level_ar = models.CharField(max_length=50)  
    skill_level_en = models.CharField(max_length=50)  

    def __str__(self):
        return self.skill_name_ar

class Education(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    school_name_ar = models.CharField(max_length=100)  
    school_name_en = models.CharField(max_length=100)  
    degree_ar = models.CharField(max_length=50)  
    degree_en = models.CharField(max_length=50)  
    period_ar = models.CharField(max_length=50)  
    period_en = models.CharField(max_length=50)  
    details_ar = models.CharField(max_length=50)  
    details_en = models.CharField(max_length=50)  

    def __str__(self):
        return self.school_name_ar

class Experience(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    job_description_ar = models.CharField(max_length=50)  
    job_description_en = models.CharField(max_length=50)  
    company_name_ar = models.CharField(max_length=100)  
    company_name_en = models.CharField(max_length=100)  
    position_ar = models.CharField(max_length=50)  
    position_en = models.CharField(max_length=50)  
    period_ar = models.CharField(max_length=50)  
    period_en = models.CharField(max_length=50)  
    details_ar = models.CharField(max_length=250)  
    details_en = models.CharField(max_length=250)  

    def __str__(self):
        return self.company_name_ar

class Works(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title_ar = models.CharField(max_length=50)  
    title_en = models.CharField(max_length=50)  
    description_ar = models.CharField(max_length=200)  
    description_en = models.CharField(max_length=200)  
    technical_ar = models.CharField(max_length=50)  
    technical_en = models.CharField(max_length=50)  
    image_project = models.ImageField(upload_to='projects/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return self.title_ar
