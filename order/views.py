from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.shortcuts import render
from car.models import Car
from book.models import Book
from datetime import datetime, date, timedelta
from django.db.models import Q

class HomeView(TemplateView):
    template_name = "order/index.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        favorite_cars = request.user.favorites.all()
        today = datetime.today()
        if "narrow_start_datetime" in request.session.keys() and "narrow_end_datetime" in request.session.keys():
            narrow_start_datetime = request.session["narrow_start_datetime"]
            narrow_end_datetime = request.session["narrow_end_datetime"]
        else:
            narrow_start_datetime = datetime.strftime(today, '%Y-%m-%dT%H:%m')
            narrow_end_datetime = datetime.strftime(today+timedelta(days=1), '%Y-%m-%dT%H:%m')
        # cars = Car.objects.filter(group=request.user.active_group)
        books = Book.objects.exclude(Q(group=request.user.active_group, end_datetime__lt=narrow_start_datetime) | Q(group=request.user.active_group, start_datetime__gt=narrow_end_datetime))
        cars = [car for car in Car.objects.filter(group=request.user.active_group) if car.pk not in [book.car.pk for book in books]]
        return render(request, self.template_name, {
            "cars": cars,
            "favorite_cars": favorite_cars,
            "narrow_start_datetime": narrow_start_datetime,
            "narrow_end_datetime": narrow_end_datetime,
        })

    def post(self, request, **kwargs):
        if self.request.POST['action'] == 'add_favorite':
            favorite_car = Car.objects.get(pk=self.request.POST['car_pk'], group=request.user.active_group)
            favorite_car.favorites.add(request.user)
            favorite_car.save()
        elif self.request.POST['action'] == 'remove_favorite':
            favorite_car = Car.objects.get(pk=self.request.POST['car_pk'], group=request.user.active_group)
            favorite_car.favorites.remove(request.user)
            favorite_car.save()
        elif self.request.POST['action'] == 'booking':
            request.session['car_pk'] = self.request.POST['car_pk']
            return redirect('book:booking')
        elif self.request.POST['action'] == 'narrow':
            request.session["narrow_start_datetime"] = self.request.POST['narrow_start_datetime']
            request.session["narrow_end_datetime"] = self.request.POST['narrow_end_datetime']
        return redirect('order:home')
