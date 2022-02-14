from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from account import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    url(r'^account/',include('account.urls')),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^login/',views.user_login,name='user_login'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_DIR)