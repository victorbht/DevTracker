from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import StudySession, UserProfile, UserInventory, PerfilUsuario

XP_MULTIPLIERS = {
    'VIDEO': 1.0, 'READING': 1.2, 'CODING': 1.5, 'PROJECT': 2.0
}

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.get_or_create(user=instance)
        UserProfile.objects.get_or_create(user=instance)
        UserInventory.objects.get_or_create(user=instance)

@receiver(post_save, sender=StudySession)
def calculate_rewards(sender, instance, created, **kwargs):
    if created:
        profile = instance.user.profile
        today = timezone.now().date()
        
        # === LÓGICA DE STREAK ===
        if profile.last_checkin == today:
            pass  # Já contou hoje
        elif profile.last_checkin == today - timedelta(days=1):
            # Veio ontem, streak continua!
            profile.current_streak += 1
            profile.last_checkin = today
            # Bônus de Streak (ex: +5 moedas por dia de streak, max 50)
            bonus = min(profile.current_streak * 5, 50)
            profile.dev_coins += bonus
        else:
            # Quebrou o streak... tem congelador?
            if profile.streak_freezes > 0:
                profile.streak_freezes -= 1
                # Mantém o streak, só atualiza a data
                profile.last_checkin = today
            else:
                # Perdeu tudo :(
                profile.current_streak = 1
                profile.last_checkin = today
        
        if profile.current_streak > profile.longest_streak:
            profile.longest_streak = profile.current_streak
        
        # === LÓGICA DE XP & LEVELS ===
        # 1. Calcular XP
        base_xp = instance.duration_minutes
        multiplier = XP_MULTIPLIERS.get(instance.method, 1.0)
        final_xp = int(base_xp * multiplier)
        
        # 2. Calcular Moedas (1 a cada 5 min)
        coins = int(instance.duration_minutes / 5)
        
        # 3. Atualizar Registro
        StudySession.objects.filter(pk=instance.pk).update(xp_earned=final_xp, coins_earned=coins)
        
        # 4. Atualizar Perfil
        profile.current_xp += final_xp
        profile.total_xp += final_xp
        profile.dev_coins += coins
        
        # 5. Level Up Logic
        while profile.current_xp >= profile.xp_to_next_level():
            profile.current_xp -= profile.xp_to_next_level()
            profile.level += 1
        
        profile.save()
        
        # === LÓGICA DE BADGES ===
        try:
            from .achievements import check_achievements
            check_achievements(instance.user, instance)
        except ImportError:
            pass  # achievements.py ainda não existe
