from django.contrib import admin
from django.urls import path, include

from echoserver.views import homePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('echo.urls'))
]

