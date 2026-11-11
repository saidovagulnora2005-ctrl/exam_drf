from django.contrib.auth.models import BaseUserManager
from rest_framework.response import Response


class CustomUserManager(BaseUserManager):
    def _create_user(self,email,password, **extra_fields):
        if not email:
            return Response({'error': 'Email must be set!'})

        email = self.normalize_email(email=email)
        user.set_password(password)
        user = self.model(email=email,password=password,**extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self,email,password,**extra_fields):
        extra_fields.setdefault('is_active', False)
        if extra_fields.get('is_active') is not False:
            extra_fields['is_active'] = False
        return self._create_user(email=email,password=password, **extra_fields)
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_active') is not True:
            raise ValueError('Status is active must be True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Status is staff must be True')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Status is superuser must be True')
        
        return self._create_user(email=email,password=password, **extra_fields)

    