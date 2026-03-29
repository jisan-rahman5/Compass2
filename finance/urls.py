from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.finance_overview, name='overview'),
    path('expense/add/', views.expense_add, name='expense_add'),
    path('expense/<int:pk>/edit/', views.expense_edit, name='expense_edit'),
    path('expense/<int:pk>/delete/', views.expense_delete, name='expense_delete'),
    path('income/', views.income_manage, name='income'),
    path('income/<int:pk>/edit/', views.income_manage, name='income_edit'),
    path('income/<int:pk>/delete/', views.income_delete, name='income_delete'),
    path('export/', views.export_finances_csv, name='export_csv'),
]
