from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.employee_form, name='employee_insert'),
    path('<int:id>/', views.employee_form, name='employee_update'),
    path('delete/<int:id>/', views.employee_delete, name='employee_delete'),
    path('list/', views.employee_List, name='employee_list'),
    path('ics/', views.ics_create, name='ics_create'),
    path('ics_send/', views.ics_send, name='ics_send')
]