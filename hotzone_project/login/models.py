from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator

# Create your models here.
class StaffManager(BaseUserManager):
    def create_user(self, staff_number, username, password):
        if not username:
            raise ValueError("User must have an username.")
        if not password:
            raise ValueError("User must have a password.")
        if not staff_number:
            raise ValueError("User must have a staff_number.")

        user = self.model(
            username = username,
            staff_number = staff_number
        )

        user.set_password(password)

        user.save(using=self._db)
        return user
    
    def create_superuser(self, staff_number, username, password):
        user = self.create_user(
            staff_number = staff_number,
            username = username,
            password = password
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

class Staff(AbstractBaseUser):
    staff_number = models.CharField(max_length=7, validators=[MinLengthValidator(7)], unique=True)

    username=models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    first_name=models.CharField(max_length=100)
    last_name = models.CharField(max_length=50)

    email = models.EmailField(verbose_name='email', max_length = 254, unique=True)

    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
    is_admin = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'staff_number']

    objects = StaffManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True