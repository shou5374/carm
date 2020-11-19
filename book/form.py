from django import forms
from book.models import Book
from car.models import Car
from users.models import User, UserGroup
from django.utils.translation import gettext, gettext_lazy as _
from django.db.models import Q
from datetime import datetime, date, timedelta

       
class BookingForm(forms.Form):
        
    car_name = forms.CharField(
        label=_('車両番号'),
        widget=forms.TextInput(attrs={
            'readonly': True,
        }),
    )

    user_name = forms.CharField(
        label=_('登録者名'),
        widget=forms.TextInput(attrs={
            'readonly': True,
        }),
    )
    
    group_name = forms.CharField(
        label=_('組織名'),
        max_length=17,
        widget=forms.TextInput(attrs={
            'readonly': True,
        }),
    )

    driver_name = forms.CharField(
        label=_('運転者氏名'),
        max_length=17,
        widget=forms.TextInput(attrs={
        }),
        required=True,
    )
    
    start_datetime = forms.DateTimeField(
        label=_('借用日時'),
        widget=forms.TextInput(attrs={
            "type": "datetime-local",
        }),
        required=True,
    )

    end_datetime = forms.DateTimeField(
        label=_('返却日時'),
        widget=forms.TextInput(attrs={
            "type": "datetime-local",
        }),
        required=True,
    )

    class Meta:
        model = Book
        fields = ['car_name', 'user_name', 'group_name', 'driver_name', 'start_datetime', 'end_datetime',]

    def clean(self):
        data = self.cleaned_data
        group = UserGroup.objects.get(name=data["group_name"])
        car = Car.objects.get(name=data['car_name'], group=group)
        user = User.objects.get(username=data['user_name'])
        books = Book.objects.filter(car=car)
        books = books.exclude(Q(end_datetime__lt=data['start_datetime']) | Q(start_datetime__gt=data['end_datetime']))
        if books.exists():
            self.add_error(None, '他の予約と時間帯が重複しています')
        if data['start_datetime'] >= data['end_datetime']:
            self.add_error(None, '開始時間と終了時間に矛盾があります')
        return self.cleaned_data

    def save(self):
        data = self.cleaned_data
        group = UserGroup.objects.get(name=data["group_name"])
        car = Car.objects.get(name=data['car_name'], group=group)
        user = User.objects.get(username=data['user_name'])
        new_book = Book.objects.create(car=car, user=user, group=group, driver_name=data['driver_name'], start_datetime=data['start_datetime'], end_datetime=data['end_datetime'])
        new_book.save()
        return new_book
