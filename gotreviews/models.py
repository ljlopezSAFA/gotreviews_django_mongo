from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django_mongodb_backend.fields import ArrayField
from django_mongodb_backend.models import EmbeddedModel


#Create your models here.

#SQLITE MODELS
class UserManager(BaseUserManager):
    def create_user(self, mail, username, role, password=None):
        if not mail or not username or not role:
            raise ValueError("Debes rellenar los campos requeridos (mail, username, role)")
        mail = self.normalize_email(mail)
        user = self.model(email=mail, nombre=username, rol=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mail, username, role='admin', password=None):
        user = self.create_user(mail, username, role, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
    )

    mail = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default='cliente')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mail',  'role']

    def __str__(self):
        return self.username



#MONGODB MODELS
class BrotherHoods(models.Model):
    code= models.IntegerField(null=False)
    name= models.CharField(max_length=150)
    logo= models.URLField(max_length=900)
    day = models.CharField(max_length=300)


    class Meta:
        db_table = 'brotherhoods'
        managed = False

    def __str__(self):
        return self.name


class Category(models.Model):
    code = models.IntegerField(null=False, unique=True)
    name= models.CharField(max_length=150, unique=True)
    description= models.CharField(max_length=300)
    logo  = models.CharField(max_length=900)
    brotherhoods = ArrayField(models.IntegerField(), null=True, blank=True, default=list)

    class Meta:
        db_table = 'categories'
        managed = False

    def __str__(self):
        return self.name


class Review(models.Model):
   user = models.CharField(max_length=150)
   characterCode = models.IntegerField(null=False)
   reviewDate = models.DateField(default=timezone.now)
   rating = models.PositiveIntegerField(null=False,  validators=[MinValueValidator(1), MaxValueValidator(5)])
   comments = models.TextField()

   def __str__(self):
       return self.user + " " + str(self.rating)

   class Meta:
       db_table = 'reviews'
       managed = False


class Ranking(models.Model):
    user = models.CharField(max_length=150)
    rankinDate = models.DateField(default=timezone.now)
    categoryCode = models.IntegerField(null=False)
    rankinList = ArrayField(models.JSONField(), null=True, blank=True, default=list)

    def __str__(self):
        return self.user +  str(self.categoryCode)

    class Meta:
        db_table = 'rankings'
        managed = False




