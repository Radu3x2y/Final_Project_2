from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView
from user import views
from user.views import EmployeeCreateView, CustomLoginView, SupervisorCreateView

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('login'), permanent=False)),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('overview/', views.overview, name='overview'),
    path('create_user_employee/', EmployeeCreateView.as_view(), name='create-user-employee'),
    path('create_user_supervisor/', SupervisorCreateView.as_view(), name='create-user-supervisor'),
]
