from django.contrib import admin
from .models import Book, Passing, Breaking

# Register your models here.
admin.site.register(Book)
admin.site.register(Passing)
admin.site.register(Breaking)
