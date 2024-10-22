"""
URL configuration for rasapalembang project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from rasapalembang.views import landing
from django.urls import path, include
from authentication.views import (
    detail_profile,
    profile,
    signup,
    login,
    logout,
)
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path("", landing, name="landing"),
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/<slug:username>', detail_profile, name='detail_profile'),
    path('restoran/', include('restoran.urls')), 
    path('restoran/<uuid:id_restoran>/forum/', include('forum.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
