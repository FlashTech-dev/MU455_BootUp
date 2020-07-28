from django.contrib import admin
from django.urls import path, include


from django.contrib.auth import views as auth_views
from user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    

    # User Urls
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('register/', user_views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'user/logout.html'), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'user/password_reset.html'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'user/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'user/password_reset_complete.html'), name="password_reset_complete"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'user/password_reset_confirm.html'), name="password_reset_confirm"),

    # Pages Urls
    path('team/', user_views.team, name='team'),
    path('docs/', user_views.docs, name='docs'),
    path('how-we-do-it/', user_views.hwdi, name='hwdi'),
    path('faq/', user_views.faq, name='faq'),

    # @login_required
    path('', user_views.home, name='home'),
    path('profile/', user_views.profile, name='profile'),

    # API
]

