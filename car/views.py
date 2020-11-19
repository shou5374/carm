from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from car.models import Car, CarType

class ManageCarView(TemplateView):
    template_name = "car/manage_car.html"
    error_template_name = "car/manage_car.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if request.user != request.user.active_group.leader:
            return redirect('order:home')
        group = request.user.active_group
        cars = Car.objects.filter(group=group)
        car_types = CarType.objects.all()
        error_list = None
        if 'error_list' in request.session.keys():
            error_list = request.session['error_list']
            del request.session['error_list']
        return render(request, self.template_name, {
            "cars": cars,
            "car_types": car_types,
            "error_list": error_list,
        })

    def post(self, request, **kwargs):
        if self.request.POST['action'] == 'add':
            name = self.request.POST['name']
            group = request.user.active_group
            category = CarType.objects.get(pk=self.request.POST['category'])
            image = self.request.FILES['image']
            if Car.objects.filter(name=name, group=group).exists():
                request.session['error_list'] = ["既に存在する車両番号です", ]
            else:
                new_car = Car.objects.create(name=name, group=group, category=category, image=image)
                new_car.save()
        elif self.request.POST['action'] == 'remove':
            car = Car.objects.get(pk=self.request.POST['car_pk'])
            car.delete()
        return redirect('car:manage_car')