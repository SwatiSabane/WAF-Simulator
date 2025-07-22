from django.urls import path
from . import views

urlpatterns = [
    path('', views.input_form, name='input_form'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-rule/', views.add_rule, name='add_rule'),
    path('delete-rule/<int:rule_id>/', views.delete_rule, name='delete_rule'),
    path('toggle-rule/<int:rule_id>/', views.toggle_rule, name='toggle_rule'),
]
