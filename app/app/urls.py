from django.contrib import admin
from django.urls import path

from django.contrib.auth import views as auth_views
from user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    

    # User Urls
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('register/', user_views.register, name='register'),

    path('team/', user_views.team, name='team'),
    path('docs/', user_views.docs, name='docs'),
    path('hwdi/', user_views.hwdi, name='hwdi'),
    path('faq/', user_views.faq, name='faq'),
]
