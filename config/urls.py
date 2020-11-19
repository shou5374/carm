from django.contrib import admin
from django.urls import path, include

# mediaから画像を読み込む用
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('order.urls')),
    path('users/', include('users.urls')),
    path('book/', include('book.urls')),
    path('car/', include('car.urls')),
]

# mediaから画像を読み込む用
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
