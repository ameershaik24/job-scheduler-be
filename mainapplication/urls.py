from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('jobscheduler/', include('jobscheduler.urls')),
    path('admin/', admin.site.urls),
]