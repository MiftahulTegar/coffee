from django.conf.urls import url
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'account'

urlpatterns=[
    # Login dan Register
    path('user_login/', auth_views.LoginView.as_view(), name='user_login'), 
    path('register/',views.register,name='register'), 
    path('', views.dashboard, name='dashboard'),

    # Produk
    path('produk/', views.produk, name='produk'),
    path('coffee/', views.coffee, name='coffee'),
    path('frappe/', views.frappe, name='frappe'),
    path('non_coffee/', views.non_coffee, name='non_coffee'),

    # Profile dan Blog
    path('edit/', views.edit, name='edit'),
    path('profile/', views.profile, name='profile'),
    path('blog/', views.blog, name='blog'),

    # Reset Password
    path('password_reset/',
        auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('account:password_reset_done')),
        name='password_reset'),
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('account:password_reset_complete')),
        name='password_reset_confirm'),
    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),

    # Ubah Password
    path('password_change/',
        auth_views.PasswordChangeView.as_view(
        success_url=reverse_lazy('account:password_change_done')),
        name='password_change'),
    path('password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'),

    # Link to Page
    path('<slug:post>/',views.post_detail, name='post_detail'),
]