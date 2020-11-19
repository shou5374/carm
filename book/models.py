from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User, UserGroup
from car.models import Car
from django.utils import timezone

class Breaking(models.Model):
    start_time = models.DateTimeField(
        _("開始時刻"),
        default=timezone.now,
    )
    end_time = models.DateTimeField(
        _("終了時刻"),
        default=timezone.now,
    )
    point = models.CharField(
        _('地点'),
        max_length=17,
        default="記録なし",
    )
    
    class Meta:
        verbose_name = _('braking')

    def __str__(self):
        return self.point

class Passing(models.Model):
    start_point = models.CharField(
        _('発地'),
        max_length=17,
        default="記録なし",
    )
    end_point = models.CharField(
        _('着地'),
        max_length=17,
        default="記録なし",
    )
    has_bag = models.BooleanField(
        _('積載状況'),
        default=False,
    )

    class Meta:
        verbose_name = _('passing')

    def __str__(self):
        return self.start_point + "~" + self.end_point

class Book(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='booked_car')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booked_user')
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, related_name='booked_group')
    driver_name = models.CharField(
        _('driver_name'),
        max_length=17,
    )
    start_datetime = models.DateTimeField(
        _("借用日時"),
    )
    end_datetime = models.DateTimeField(
        _("返却日時"),
    )

    # 追加情報
    distance = models.IntegerField(
        _('走行距離'),
        blank=True,
        default=0,        
    )
    oil = models.IntegerField(
        _('補給量'),
        blank=True,
        default=0,
    )
    toll = models.IntegerField(
        _('通行料金(ETC)'),
        blank=True,
        default=0,
    )

    passings = models.ManyToManyField(
        Passing, 
        blank=True, 
        related_name='passings'
    )
    breakings = models.ManyToManyField(
        Breaking, 
        blank=True, 
        related_name='breakings'
    )

    class Meta:
        verbose_name = _('book')

    def __str__(self):
        return self.car.name
