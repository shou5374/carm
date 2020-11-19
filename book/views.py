from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.shortcuts import render
from .models import Book, Passing, Breaking
from car.models import Car
from book.form import BookingForm
from datetime import datetime, date, timedelta
from collections import defaultdict
from django.http.response import HttpResponse
from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.http import FileResponse
from django.utils import timezone

class BookingView(TemplateView):
    template_name = "book/booking.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if 'car_pk' in request.session.keys():
            car_pk = request.session['car_pk']
            car = Car.objects.get(pk=car_pk)
            form = BookingForm(initial={'car_name':car.name, 'user_name':request.user.username, 'group_name':request.user.active_group.name})
        else:
            car = None
            form = None
        return render(request, self.template_name, {
            "car": car,
            "form": form,
            'schedule': self.get_schedule(car, request.user.active_group),
        })

    def post(self, request, **kwargs):
        if self.request.POST['action'] == 'booking':
            form = BookingForm(request.POST)
            if form.is_valid():
                book = form.save()
                return redirect("order:home")
            else:
                car = Car.objects.get(name=request.POST['car_name'], group=request.user.active_group)
                return render(request, self.template_name, {'car': car, 'form': form, 'schedule': self.get_schedule(car, request.user.active_group)})

    def get_schedule(self, car, group):
        today = datetime.today()
        books = Book.objects.filter(car=car, group=group, end_datetime__gt=today, start_datetime__lt=(today+timedelta(days=31)))
        schedule = defaultdict(dict)
        for i in range(31): # 1ヶ月分程度
            after_day = datetime.strftime(today + timedelta(days=i), '%m月%d日')
            for j in range(24):
                schedule[after_day][str(j).zfill(2) + ":00"] = False
        for book in books:
            start = book.start_datetime
            end_day, end_hour = datetime.strftime(book.end_datetime, '%m月%d日--%H:00').split("--")
            for i in range(31*24):
                start_day, start_hour = datetime.strftime(start, '%m月%d日--%H:00').split("--")
                if start_day == end_day and start_hour == end_hour:
                    break
                else:
                    if start_day in schedule.keys():
                        schedule[start_day][start_hour] = True
                start = start + timedelta(hours=1)

        return dict(schedule)

class ManageBookView(TemplateView):
    template_name = "book/manage_book.html"
    pdf_template_name = "book/report.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        books = Book.objects.filter(user=request.user)
        books = [(book, book.passings.all(), book.breakings.all()) for book in books]
        print(books)
        return render(request, self.template_name, {
            "books": books,
        })

    def post(self, request, **kwargs):
        if self.request.POST['action'] == 'remove':
            book_pk = self.request.POST['book_pk']
            Book.objects.get(pk=book_pk).delete()
        elif self.request.POST['action'] == 'update_info':
            book = Book.objects.get(pk=self.request.POST["book_pk"])
            book.distance = int(self.request.POST["distance"])
            book.oil = int(self.request.POST['oil'])
            book.toll = int(self.request.POST['toll'])
            book.save()
        elif self.request.POST['action'] == 'add_pass':
            pass_type = self.request.POST["pass"]
            book = Book.objects.get(pk=self.request.POST["book_pk"])
            if pass_type == 'breaking':
                start_time = self.request.POST["start_time"]
                end_time = self.request.POST["end_time"]
                point = self.request.POST["point"]
                new_breaking = Breaking.objects.create(start_time=start_time, end_time=end_time, point=point)
                new_breaking.save()
                book.breakings.add(new_breaking)
                book.save()
            else:
                start_point = self.request.POST["start_point"]
                end_point = self.request.POST["end_point"]
                has_bag = True if self.request.POST["has_bag"] == "1" else False
                new_passing = Passing.objects.create(start_point=start_point, end_point=end_point, has_bag=has_bag)
                new_passing.save()
                book.passings.add(new_passing)
                book.save()
        elif self.request.POST['action'] == 'report':
            book = Book.objects.get(pk=self.request.POST["book_pk"])
            html_template = get_template(self.pdf_template_name)
            html_str = html_template.render({
                "book": book,
                "passings": book.passings.all(),
                "breakings": book.breakings.all(),
                "create_date": timezone.now,
            }, request)
            pdf_file = HTML(string=html_str, base_url=request.build_absolute_uri()).write_pdf()
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'filename="report.pdf"'
            return response
        return redirect("book:manage_book")

class AddInfoView(TemplateView):
    template_name = "book/add_info.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if 'book_pk' not in request.session.keys():
            return redirect('manage_book')
        book_pk = request.session['book_pk']
        return render(request, self.template_name, {
        })

    def post(self, request, **kwargs):
        if self.request.POST['action'] == 'remove':
            pass

class ReportView(TemplateView):
    template_name = "book/report.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if 'book_pk' not in request.session.keys():
            return redirect('manage_book')
        book_pk = request.session['book_pk']
        return render(request, self.template_name, {
        })

    def post(self, request, **kwargs):
        if self.request.POST['action'] == 'remove':
            pass
