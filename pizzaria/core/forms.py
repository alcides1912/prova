# core/forms.py
from django import forms
from .models import Cliente, Reserva

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['user', 'telefone',]

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'mesa', 'data_reserva', 'hora_reserva', 'num_pessoas']

from .models import Mesa

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['numero', 'capacidade']  # Campos da tabela Mesa