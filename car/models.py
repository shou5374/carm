from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User, UserGroup

class CarType(models.Model):
    name = models.CharField(
        _('name'),
        max_length=10,
        help_text=_('Required. 10 characters or fewer.'),
        unique=True,
    )

    class Meta:
        verbose_name = _('car_type')

    def __str__(self):
        return self.name

class Car(models.Model):
    name = models.CharField( # 車両番号
        _('name'),
        max_length=17,
        help_text=_('Required. 17 characters or fewer.'),
        unique=True,
    )
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, related_name='group')
    category = models.ForeignKey('CarType', on_delete=models.CASCADE, related_name='category')
    image = models.ImageField(upload_to='images/users', default="images/car/default_car.jpg")
    favorites = models.ManyToManyField(User, blank=True, related_name='favorites') 

    class Meta:
        verbose_name = _('car')

    def __str__(self):
        return self.name

