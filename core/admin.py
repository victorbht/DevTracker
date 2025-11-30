from django.contrib import admin
from django import forms
from .models import (
    Tecnologia, MetodoEstudo, SessaoEstudo, Conquista, PerfilUsuario,
    SkillNode, UserProfile, StudySession, StoreItem, UserInventory,
    JobQuest, BossBattle, ProjectSubmission, CodeReview, Badge, UserBadge
)

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

# === GAMIFICAÇÃO ORIGINAL ===
@admin.register(Conquista)
class ConquistaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'quantidade_necessaria', 'xp_reward', 'oculta')
    list_filter = ('categoria', 'oculta')

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'xp_total', 'nivel', 'meta_semanal', 'meta_mensal')
    filter_horizontal = ('conquistas',)

# === PACOTE GAMER ===
@admin.register(SkillNode)
class SkillNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'icon_class')
    list_filter = ('parent',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'xp_bonus', 'coin_bonus', 'is_secret')
    list_filter = ('is_secret',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'badge', 'earned_at')
    list_filter = ('badge', 'earned_at')
    date_hierarchy = 'earned_at'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'current_xp', 'total_xp', 'dev_coins', 'current_streak')
    list_filter = ('level',)
    filter_horizontal = ('skills_desbloqueadas',)
    readonly_fields = ('total_xp', 'longest_streak')

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'method', 'duration_minutes', 'xp_earned', 'coins_earned', 'start_time')
    list_filter = ('method', 'skill', 'start_time')
    readonly_fields = ('duration_minutes', 'xp_earned', 'coins_earned')
    date_hierarchy = 'start_time'

@admin.register(StoreItem)
class StoreItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)

@admin.register(UserInventory)
class UserInventoryAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('items',)

@admin.register(JobQuest)
class JobQuestAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'min_level', 'required_skill', 'is_active')
    list_filter = ('is_active', 'min_level', 'required_skill')

@admin.register(BossBattle)
class BossBattleAdmin(admin.ModelAdmin):
    list_display = ('title', 'xp_reward')

@admin.register(ProjectSubmission)
class ProjectSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'boss', 'sos_requested', 'created_at')
    list_filter = ('sos_requested', 'boss')
    date_hierarchy = 'created_at'

@admin.register(CodeReview)
class CodeReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'submission', 'role', 'is_accepted')
    list_filter = ('role', 'is_accepted')