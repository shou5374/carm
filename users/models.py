from django.apps import apps
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator


class UserManager(BaseUserManager):
    """カスタムユーザーマネージャーモデル"""
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル"""
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=30,
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
    )
    email = models.EmailField(_('email address'), unique=True)
    #フォロイーフィールドをUser自身に持たせる
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    user_image = models.ImageField(upload_to='images/users', default="images/users/default_user.jpeg")
    active_group = models.ForeignKey('UserGroup', on_delete=models.SET_NULL, null=True, related_name='active_group')

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class UserGroup(models.Model):
    name = models.CharField(
        _('name'),
        max_length=15,
        help_text=_('Required. 15 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        unique=True,
    )
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leader')
    members = models.ManyToManyField(User, blank=True, related_name='members') # 承認済みメンバー
    unapproved_members = models.ManyToManyField(User, blank=True, related_name='unapproved_members') # 未承認メンバー

    class Meta:
        verbose_name = _('user_group')

    def __str__(self):
        return self.name
