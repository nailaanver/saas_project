from django.urls import path
from . import views_frontend

urlpatterns = [
    path("workspace/<int:tenant_id>/",views_frontend.workspace_dashboard,name='workspace_dashboard'),
]