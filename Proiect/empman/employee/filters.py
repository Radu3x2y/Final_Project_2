import django_filters
from django import forms

from employee.models import Employee


class EmployeeFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains', label="First name", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Search first name'}))
    last_name = django_filters.CharFilter(lookup_expr='icontains', label="Last name", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Search last name'}))
