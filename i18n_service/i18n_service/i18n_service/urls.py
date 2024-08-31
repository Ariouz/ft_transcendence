"""
URL configuration for i18n_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from i18n_service_app.views import translations_view, translation_by_key_view, languages_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('translations/<str:lang_code>/', translations_view, name='translations_view'),
    path('translations/<str:lang_code>/<str:key>/', translation_by_key_view, name='translation_by_key_view'),
    path('languages/', languages_view, name='languages_view'),
]
