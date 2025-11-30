from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Tecnologia(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    def __str__(self): return self.nome

class MetodoEstudo(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    def __str__(self): return self.nome

class SessaoEstudo(models.Model):
    tecnologia = models.ForeignKey(Tecnologia, on_delete=models.CASCADE, verbose_name="Matéria")
    topico = models.CharField(max_length=100, verbose_name="Conteúdo") 
    metodo = models.ForeignKey(MetodoEstudo, on_delete=models.SET_NULL, null=True, verbose_name="Método")
    data_registro = models.DateTimeField(default=timezone.now, verbose_name="Data/Hora Início")
    tempo_liquido = models.DurationField(help_text="Formato HH:MM:SS")
    qtd_exercicios = models.IntegerField(default=0, verbose_name="Qtd. Exercícios", blank=True)
    qtd_acertos = models.IntegerField(default=0, verbose_name="Qtd. Acertos", blank=True)
    anotacoes = models.TextField(blank=True, verbose_name="Diário de Bordo (Markdown)")

    class Meta:
        ordering = ['-data_registro']
        indexes = [
            models.Index(fields=['data_registro']),
            models.Index(fields=['tecnologia']),
            models.Index(fields=['metodo']),
        ]
    def __str__(self): return f"{self.tecnologia} - {self.topico}"

# === MODELOS DE GAMIFICAÇÃO ===
class Conquista(models.Model):
    CATEGORIAS = [
        ('tempo', 'Tempo Total'),
        ('tecnologia', 'Especialista em Tecnologia'),
        ('metodo', 'Mestre do Método'),
        ('streak', 'Ofensiva'),
    ]
    TIPOS_VISUAIS = [
        ('padrao', 'Círculo Padrão'),
        ('hexagono', 'Hexágono (Desafio)'),
    ]
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    tipo_visual = models.CharField(max_length=20, choices=TIPOS_VISUAIS, default='padrao')
    tecnologia_alvo = models.ForeignKey(Tecnologia, on_delete=models.CASCADE, null=True, blank=True)
    metodo_alvo = models.ForeignKey(MetodoEstudo, on_delete=models.CASCADE, null=True, blank=True)
    quantidade_necessaria = models.IntegerField()
    xp_reward = models.IntegerField(default=100)
    icone_fa = models.CharField(max_length=50, default="fas fa-trophy")
    cor_hex = models.CharField(max_length=7, default="#f1c40f")
    oculta = models.BooleanField(default=False, help_text="Quando marcada, só aparece após desbloquear.")
    def __str__(self): return self.nome

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    xp_total = models.IntegerField(default=0)
    nivel = models.IntegerField(default=1)
    conquistas = models.ManyToManyField(Conquista, blank=True)
    meta_semanal = models.IntegerField(default=0, help_text="Meta em horas")
    meta_mensal = models.IntegerField(default=0, help_text="Meta em horas")
    def __str__(self): return f"Perfil de {self.user.username}"

# Sinais para criar Perfil automaticamente
@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created: PerfilUsuario.objects.create(user=instance)
@receiver(post_save, sender=User)
def salvar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()
