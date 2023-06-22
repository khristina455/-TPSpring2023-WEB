"""
URL configuration for askme project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from logging import DEBUG

from askme import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from askmeWEB import views
#home/khristina/PycharmProjects/pythonProject/-TPSpring2023-WEB/askme/nginx.conf
urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('question/<int:question_id>/', views.question, name="question"),
    path('ask/', views.ask, name="ask"),
    path('login/', views.login, name="login"),
    path('singup/', views.singup, name="singup"),
    path('hot/', views.hot, name="hot"),
    path('tag/<str:tag>/', views.tag, name="tag"),
    path('logout/', views.logout, name='logout'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('vote/', views.vote, name='vote'),
    path('correct/', views.correct, name='correct')
]

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
#    urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
