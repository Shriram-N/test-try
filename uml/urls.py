from django.contrib import admin
from django.urls import path,include
from . import views


app_name = 'books'
urlpatterns = [
    #path('review/', include('books.urls'))
    path('', views.services_list, name='services_list'),
    path('service/<str:service>', views.service_detail, name='service_detail'),
    path('service/<str:service>/<str:controller_name>/<str:method_name>', views.diagrams, name='diagrams'),

]
