

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, mobile_number, password,name,email ):
        if not mobile_number:
            raise ValueError("Mobile number is required.")
        if not password:
            raise ValueError("password is required.")
        if not name:
            raise ValueError("name is required.")
        if not email:
            raise ValueError("email is required.")
       
        
        user = self.model(
                           mobile_number=mobile_number,
                           username=mobile_number,
                           name=name,
                           email=email,
                         )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password,name,email):
        user = self.create_user(mobile_number, password, name,email)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user




class User(AbstractUser):
    mobile_number = models.CharField(max_length=11, null=False, unique=True)
    otp = models.CharField(max_length=6,blank=True)
    name=models.CharField( max_length=50, blank=False)
    email =models.CharField(max_length=100,blank=False)
    email_is_varifaied=models.BooleanField(default=False)
    flag=models.BooleanField(default=False)
    profile_picture=models.ImageField(upload_to='images/user_profile_Pic',default='static_files/images/student_image.jpeg')
    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = ['name','email']
    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.name}"
    


