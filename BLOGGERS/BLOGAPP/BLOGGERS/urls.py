from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('BLOGAPP.urls')),
    path('Members/', include('django.contrib.auth.urls')),
    path('Members/', include('Members.urls')),

]
