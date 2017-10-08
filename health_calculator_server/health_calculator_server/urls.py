"""health_calculator_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from server import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^show',views.data_save),
    url(r'^so2',views.graph_so2),
    url(r'^o3',views.graph_o3),
    url(r'^no2',views.graph_no2),
    url(r'^co',views.graph_co),
    url(r'^pm25',views.graph_pm25),
    url(r'^pie',views.pie_chart),
    url(r'^pa',views.predictive_analytics)
]
