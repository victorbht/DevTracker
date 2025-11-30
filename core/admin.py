from django.contrib import admin
from django import forms
from .models import Tecnologia, MetodoEstudo, SessaoEstudo

class SessaoEstudoForm(forms.ModelForm):
    class Meta:
        model = SessaoEstudo
        fields = '__all__'
        widgets = {
            'anotacoes': forms.Textarea(attrs={
                'class': 'vLargeTextField',
                'style': 'font-family: monospace; width: 100%;',
                'placeholder': 'Use ``` para inserir blocos de código...'
            })
        }

@admin.register(SessaoEstudo)
class SessaoEstudoAdmin(admin.ModelAdmin):
    form = SessaoEstudoForm
    list_display = ('tecnologia', 'topico', 'metodo', 'data_registro', 'tempo_liquido', 'qtd_exercicios')
    list_filter = ('tecnologia', 'metodo', 'data_registro')
    date_hierarchy = 'data_registro'

admin.site.register(Tecnologia)
admin.site.register(MetodoEstudo)