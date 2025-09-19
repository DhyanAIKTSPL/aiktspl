"""
URL patterns for employee management APIs.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('departments/', views.DepartmentListCreateView.as_view(), name='department_list'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    path('positions/', views.PositionListCreateView.as_view(), name='position_list'),
    path('employee-details/', views.EmployeeDetailListView.as_view(), name='employee_detail_list'),
]
