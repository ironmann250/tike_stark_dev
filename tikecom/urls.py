"""tikecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from tickapp import views as tickapp_views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',auth_views.login, {'template_name': 'html/essay/login.html'}),
    url(r'^logout/$',auth_views.logout, {'next_page': '/login/'}),
    url(r'^sell/',tickapp_views.sell),
    url(r'^transfer/',tickapp_views.transfer),
    url(r'^restore/',tickapp_views.restore),
    url(r'^check/',tickapp_views.check),
    url(r'^applogin/',tickapp_views.applogin),
    url(r'^result/',tickapp_views.result),

]
