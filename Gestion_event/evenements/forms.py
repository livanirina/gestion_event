from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur
from .models import Evenement

class InscriptionForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'password1', 'password2']

    
class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ['titre', 'image', 'description', 'lieu', 'date', 'capacite', 'programme']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }