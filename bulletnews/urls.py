from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', include('web.urls')),
    path('admin/', admin.site.urls),
]
