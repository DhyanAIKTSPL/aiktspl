"""
URL patterns for salary management APIs.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('structures/', views.SalaryStructureListCreateView.as_view(), name='salary_structures'),
    path('employee-salaries/', views.EmployeeSalaryListView.as_view(), name='employee_salaries'),
    path('payroll/', views.PayrollListCreateView.as_view(), name='payroll'),
]
