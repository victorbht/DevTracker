from django import forms
from .models import SessaoEstudo, Tecnologia, MetodoEstudo
from datetime import datetime

class SessaoEstudoForm(forms.ModelForm):
    data_registro = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        label="Data/Hora Início"
    )

    class Meta:
        model = SessaoEstudo
        fields = ['tecnologia', 'topico', 'metodo', 'data_registro', 'tempo_liquido', 'qtd_exercicios', 'qtd_acertos', 'anotacoes']
        widgets = {
            'topico': forms.TextInput(attrs={'placeholder': 'Ex: Views, Joins, Flexbox'}),
            'tempo_liquido': forms.TextInput(attrs={'placeholder': 'HH:MM:SS (Ex: 01:30:00)'}),
            'anotacoes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Diário de Bordo (Markdown)...'}),
        }

# === NOVOS FORMULÁRIOS ===
class TecnologiaForm(forms.ModelForm):
    class Meta:
        model = Tecnologia
        fields = ['nome']

class MetodoForm(forms.ModelForm):
    class Meta:
        model = MetodoEstudo
        fields = ['nome']