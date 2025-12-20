from django.urls import path
from . import views

urlpatterns = [
    path('health/',views.health_check,name= 'health-check'),
    path('create/',views.create_tenant,name='create-tenant'),
    path('my/',views.my_tenants,name='my_tenants'),
    path('register/',views.register,name='register'),
    path('subscription/change/',views.change_subscription),
    path('users/manage/',views.manage_users),
    path('tasks/',views.view_tasks),

]