# project/urls.py

from django.contrib import admin
from django.urls import path, include
from cleanblog import views

urlpatterns = [
    path('', include('cleanblog.urls')),
    path('admin/', admin.site.urls),
    path('login/', views.login_auth, name='login'),
    path('logout/', views.logout_auth, name='logout'),
]

from django.conf.urls import handler404, handler500
handler404 = 'cleanblog.views.custom_404'
handler500 = 'cleanblog.views.custom_500'
