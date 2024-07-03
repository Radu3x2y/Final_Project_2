from django import forms
from django.contrib.auth.models import User
from supervisor.models import Supervisor


class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        exclude = ('user', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(SupervisorForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_superuser=False)
