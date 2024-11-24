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
from django.urls import path, include, re_path
from rasapalembang.views import landing, cari
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from authentication.views import (
    detail_profile,
    profile,
    signup,
    login,
    logout,
)

urlpatterns = (
    [
        path("", landing, name="landing"),
        path("admin/", admin.site.urls),
        path("signup/", signup, name="signup"),
        path("login/", login, name="login"),
        path("logout/", logout, name="logout"),
        path("profile/", profile, name="profile"),
        path("profile/<slug:username>", detail_profile, name="detail_profile"),
        path("restoran/", include("restoran.urls")),
        path("minuman/", include("minuman.urls")),
        path("makanan/", include("makanan.urls")),
        path("restoran/<uuid:id_restoran>/forum/", include("forum.urls")),
        path("favorit/", include("favorit.urls")),
        path("cari/", cari, name="cari"),
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
        re_path(
            r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}
        ),
        path("v1/restoran/", include("restoran.v1_urls")),
        path("v1/minuman/", include("minuman.v1_urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
