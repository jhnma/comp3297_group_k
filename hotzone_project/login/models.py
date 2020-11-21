from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator

# Create your models here.
class StaffManager(BaseUserManager):
    def create_user(self, staff_number, username, password, email):
        if not username:
            raise ValueError("User must have an username.")
        if not password:
            raise ValueError("User must have a password.")
        if not staff_number:
            raise ValueError("User must have a staff_number.")
        if not email:
            raise ValueError("User must have an email.")

        user = self.model(
            username = username,
            staff_number = staff_number,
            email = email,
        )

        user.set_password(password)

        user.save(using=self._db)
        return user
    
    def create_superuser(self, staff_number, username, password, email):
        user = self.create_user(
            staff_number = staff_number,
            username = username,
            password = password,
            email = email,
        )
        user.superuser = True

        user.save(using=self._db)
        return user

class Staff(AbstractBaseUser):
    staff_number = models.CharField(max_length=7, validators=[MinLengthValidator(7)], unique=True)

    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    first_name=models.CharField(max_length=100)
    last_name = models.CharField(max_length=50)

    email = models.EmailField(verbose_name='email', max_length = 254, unique=True)

    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
    admin = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=True)
    superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'staff_number', 'email']

    objects = StaffManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
