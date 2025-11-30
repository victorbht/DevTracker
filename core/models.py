from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify

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

# Sinais movidos para core/signals.py

# ============================================
# PACOTE GAMER - RPG & GAMIFICATION AVANÇADA
# ============================================

class SkillNode(models.Model):
    """Árvore de Habilidades (Ex: Python, Django, Lógica)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=50, default="fas fa-code", help_text="Classe FontAwesome")
    
    class Meta:
        verbose_name = "Nó de Habilidade"
        verbose_name_plural = "Árvore de Habilidades"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Badge(models.Model):
    """Conquistas/Badges do sistema"""
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, default="fas fa-medal")
    xp_bonus = models.IntegerField(default=100)
    coin_bonus = models.IntegerField(default=50)
    is_secret = models.BooleanField(default=False, help_text="Se true, só aparece quando ganha")
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """Ficha do Personagem - Sistema RPG Avançado"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Atributos RPG
    level = models.IntegerField(default=1, verbose_name="Nível")
    current_xp = models.IntegerField(default=0, verbose_name="XP Atual")
    total_xp = models.IntegerField(default=0, verbose_name="XP Total")
    dev_coins = models.IntegerField(default=0, verbose_name="DevCoins")
    
    # Streak Logic
    current_streak = models.IntegerField(default=0, verbose_name="Streak Atual")
    longest_streak = models.IntegerField(default=0, verbose_name="Maior Streak")
    last_checkin = models.DateField(null=True, blank=True, verbose_name="Último Check-in")
    streak_freezes = models.IntegerField(default=0, verbose_name="Congeladores")
    
    # Cosméticos Equipados
    equipped_frame = models.ForeignKey('StoreItem', null=True, blank=True, on_delete=models.SET_NULL, 
                                       related_name='users_framed', verbose_name="Moldura Equipada")
    equipped_banner = models.ForeignKey('StoreItem', null=True, blank=True, on_delete=models.SET_NULL, 
                                        related_name='users_bannered', verbose_name="Banner Equipado")
    
    # Perfil Público
    github_link = models.URLField(blank=True, verbose_name="Link GitHub")
    bio = models.TextField(blank=True, max_length=500, verbose_name="Bio")
    
    # Habilidades e Badges
    skills_desbloqueadas = models.ManyToManyField(SkillNode, blank=True, related_name='usuarios')
    badges = models.ManyToManyField(Badge, through='UserBadge', blank=True)
    
    class Meta:
        verbose_name = "Perfil Gamer"
        verbose_name_plural = "Perfis Gamer"
    
    def xp_to_next_level(self):
        """Fórmula RPG: Dificuldade aumenta com o nível"""
        return int((self.level * 100) * 1.5)
    
    def adicionar_xp(self, xp):
        """Adiciona XP e verifica level up"""
        self.current_xp += xp
        self.total_xp += xp
        while self.current_xp >= self.xp_to_next_level():
            self.current_xp -= self.xp_to_next_level()
            self.level += 1
        self.save()
    
    def __str__(self):
        return f"{self.user.username} (Lvl {self.level})"

class StudySession(models.Model):
    """Sessões de estudo com multiplicadores de XP"""
    METHODS = [
        ('VIDEO', 'Vídeo Aula (1.0x)'),
        ('READING', 'Leitura/Docs (1.2x)'),
        ('CODING', 'Codificação (1.5x)'),
        ('PROJECT', 'Projeto Prático (2.0x)'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(SkillNode, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    method = models.CharField(max_length=20, choices=METHODS, default='VIDEO')
    description = models.TextField(blank=True)
    
    # Calculados automaticamente
    duration_minutes = models.IntegerField(default=0, editable=False)
    xp_earned = models.IntegerField(default=0, editable=False)
    coins_earned = models.IntegerField(default=0, editable=False)
    
    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.duration_minutes = int(delta.total_seconds() / 60)
        super().save(*args, **kwargs)

# ============================================
# LOJA & COSMÉTICOS
# ============================================

class StoreItem(models.Model):
    TYPES = [('FRAME', 'Moldura Avatar'), ('BANNER', 'Banner Perfil'), ('THEME', 'Tema UI')]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=TYPES)
    price = models.IntegerField(default=100)
    image_url = models.URLField(blank=True)
    css_class = models.CharField(max_length=100, blank=True, help_text="Classe CSS para aplicar o estilo")
    
    def __str__(self):
        return f"{self.name} ({self.price} coins)"

class UserInventory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='inventory')
    items = models.ManyToManyField(StoreItem, blank=True)

class UserBadge(models.Model):
    """Relação entre usuário e badge com data de conquista"""
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user_profile', 'badge')
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.badge.name}"

# ============================================
# CARREIRA & QUESTS
# ============================================

class JobQuest(models.Model):
    """Vagas de Emprego gamificadas como Missões"""
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.CharField(max_length=50)
    min_level = models.IntegerField(default=1)
    required_skill = models.ForeignKey(SkillNode, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Quest: {self.title}"

class BossBattle(models.Model):
    """Desafios de Projeto (PBL)"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    xp_reward = models.IntegerField(default=500)
    boss_icon = models.CharField(max_length=50, default="fas fa-dragon")
    
    # Skill requerida e nível mínimo
    recommended_skill = models.ForeignKey(SkillNode, on_delete=models.SET_NULL, null=True, blank=True, related_name='bosses')
    min_skill_level = models.IntegerField(default=1, help_text="Nível necessário na Skill para desbloquear")
    
    def __str__(self):
        return self.title

class ProjectSubmission(models.Model):
    """Tentativa do usuário de derrotar o Boss"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boss = models.ForeignKey(BossBattle, on_delete=models.CASCADE)
    repo_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Party System
    sos_requested = models.BooleanField(default=False, help_text="Pedir ajuda para a comunidade?")

class CodeReview(models.Model):
    """Sistema de Party / Ajuda entre usuários"""
    ROLES = [('BUG', '🐛 Clérigo (Bug Fix)'), ('OPTIMIZE', '⚡ Ferreiro (Otimização)'), ('STYLE', '🎨 Bardo (Estilo)')]
    
    submission = models.ForeignKey(ProjectSubmission, related_name='reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES)
    content = models.TextField()
    is_accepted = models.BooleanField(default=False)
