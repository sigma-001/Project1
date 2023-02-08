from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import random, string
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        
        if not username:
            raise ValueError('Users must have an username')
        
        if not password:
            raise ValueError('Users must have a Password')

        user = self.model(username=username)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
    
        user = self.create_user(
            username = username,
            password = password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name='Username',
        max_length=255,
        unique=True,
    )
    
    is_admin = models.BooleanField(default = False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username}"
    
    @property
    def is_staff(self):
        return self.is_admin
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    
@receiver(post_save, sender = User)
def create_client(sender, instance, created, **kwargs):
    if created: 
        random_name = ''.join(random.choices(string.ascii_uppercase, k=10))
        
        Client.objects.create(user = instance,
                              name = random_name)
        
    
    
class Client(models.Model):
    
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 255)
    
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
    
    def __str__(self) -> str:
        return f"{self.id}. {self.name} ({self.user.username})"

class Artist(models.Model):
    
    name = models.CharField(max_length = 255)
    works = models.ManyToManyField("base.Work", blank = True)
    
    class Meta:
    
        verbose_name = "Artist"
        verbose_name_plural = "Artists"
        
    def __str__(self) -> str:
        return f"{self.id}. {self.name}"
    
    
WORK_CHOICES = [
        ('Youtube', 'Youtube'),
        ('Instagram', 'Instagram'),
        ('Other', 'Other')
    ]

class Work(models.Model):
    
    link = models.URLField()
    type = models.CharField(max_length = 100, choices = WORK_CHOICES, default = 'Other')
    
    class Meta:
        
        verbose_name = "Work"
        verbose_name_plural = "Works"
        
    def __str__(self) -> str:
        return f"{self.id}. {self.type}"
        