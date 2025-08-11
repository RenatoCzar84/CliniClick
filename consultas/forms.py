from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Paciente, User

class PacienteRegistrationForm(UserCreationForm):
    cpf = forms.CharField(max_length=14)
    data_nascimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    telefone = forms.CharField(max_length=20)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Paciente.objects.create(
                user=user,
                cpf=self.cleaned_data['cpf'],
                data_nascimento=self.cleaned_data['data_nascimento'],
                telefone=self.cleaned_data['telefone']
            )
        return user