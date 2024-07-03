from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from employee.models import Employee
from supervisor.models import Supervisor
from user.forms import EmployeeUserForm, AuthenticationCustomForm, SupervisorUserForm
from .utils import generate_unique_username


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'user/create_user_employee.html'
    model = User
    form_class = EmployeeUserForm

    def form_valid(self, form):
        if form.is_valid():
            try:
                with transaction.atomic():
                    new_employee_user = form.save(commit=False)
                    new_employee_user.first_name = new_employee_user.first_name.title()
                    new_employee_user.last_name = new_employee_user.last_name.title()

                    new_employee_user.username = generate_unique_username(new_employee_user.first_name,
                                                                          new_employee_user.last_name)
                    new_employee_user.save()

                    employee, created = Employee.objects.get_or_create(user=new_employee_user)
                    if not created:
                        employee.first_name = new_employee_user.first_name
                        employee.last_name = new_employee_user.last_name
                        employee.email = new_employee_user.email
                        employee.save()

                    self.success_url = reverse_lazy('update-employee', kwargs={'pk': new_employee_user.pk})
                    return super().form_valid(form)
            except IntegrityError:
                form.add_error(None, 'There was an error saving your data. Please try again.')
                return self.form_invalid(form)


class SupervisorCreateView(LoginRequiredMixin, CreateView):
    template_name = 'user/create_user_supervisor.html'
    model = User
    form_class = SupervisorUserForm

    def form_valid(self, form):
        if form.is_valid():
            try:
                with transaction.atomic():
                    new_supervisor_user = form.save(commit=False)
                    new_supervisor_user.first_name = new_supervisor_user.first_name.title()
                    new_supervisor_user.last_name = new_supervisor_user.last_name.title()

                    new_supervisor_user.username = generate_unique_username(new_supervisor_user.first_name,
                                                                            new_supervisor_user.last_name)
                    new_supervisor_user.save()

                    supervisor, created = Supervisor.objects.get_or_create(user=new_supervisor_user)
                    if not created:
                        supervisor.first_name = new_supervisor_user.first_name
                        supervisor.last_name = new_supervisor_user.last_name
                        supervisor.save()

                    self.success_url = reverse_lazy('login')
                    return super().form_valid(form)
            except IntegrityError:
                form.add_error(None, 'There was an error saving your data. Please try again.')
                return self.form_invalid(form)


class CustomLoginView(LoginView):
    form_class = AuthenticationCustomForm
    template_name = 'user/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('overview'))

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('overview')
        return super().dispatch(request, *args, **kwargs)


@login_required
def overview(request):
    user = request.user
    context = {}

    try:
        employee = Employee.objects.get(user=user)
        context['employee'] = employee
    except Employee.DoesNotExist:
        pass

    try:
        supervisor = Supervisor.objects.get(user=user)
        context['supervisor'] = supervisor
    except Supervisor.DoesNotExist:
        pass

    if not context:
        context['error_message'] = 'You are not registered as an employee or supervisor.'

    return render(request, 'employee/overview.html', context)
