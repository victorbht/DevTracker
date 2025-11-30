"""
Sistema de Conquistas (Badges) - DevTracker RPG
Verifica automaticamente se o usuário desbloqueou badges
"""
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import timedelta
from .models import Badge, UserBadge, StudySession

def check_achievements(user, session):
    """
    Roda toda vez que uma sessão é salva.
    Verifica se o usuário desbloqueou alguma badge.
    Retorna lista de badges novas.
    """
    profile = user.profile
    new_badges = []

    # === BADGES DE GRIND (Persistência) ===
    
    # Hello World - Primeira sessão
    if not UserBadge.objects.filter(user_profile=profile, badge__slug='hello-world').exists():
        try:
            badge = Badge.objects.get(slug='hello-world')
            UserBadge.objects.create(user_profile=profile, badge=badge)
            new_badges.append(badge)
        except Badge.DoesNotExist:
            pass

    # Maratonista - 4h seguidas
    if session.duration_minutes >= 240:
        if not UserBadge.objects.filter(user_profile=profile, badge__slug='maratonista').exists():
            try:
                badge = Badge.objects.get(slug='maratonista')
                UserBadge.objects.create(user_profile=profile, badge=badge)
                new_badges.append(badge)
            except Badge.DoesNotExist:
                pass

    # Centurião - 100h totais
    total_minutes = StudySession.objects.filter(user=user).aggregate(
        total=Sum('duration_minutes')
    )['total'] or 0
    total_hours = total_minutes / 60
    
    if total_hours >= 100:
        if not UserBadge.objects.filter(user_profile=profile, badge__slug='centuriao').exists():
            try:
                badge = Badge.objects.get(slug='centuriao')
                UserBadge.objects.create(user_profile=profile, badge=badge)
                new_badges.append(badge)
            except Badge.DoesNotExist:
                pass

    # === BADGES DE COMPORTAMENTO (Hábitos) ===
    
    # Night Owl - Estudou de madrugada (02:00-05:00)
    hour = session.start_time.hour
    if 2 <= hour <= 5:
        if not UserBadge.objects.filter(user_profile=profile, badge__slug='night-owl').exists():
            try:
                badge = Badge.objects.get(slug='night-owl')
                UserBadge.objects.create(user_profile=profile, badge=badge)
                new_badges.append(badge)
            except Badge.DoesNotExist:
                pass

    # Early Bird - Estudou antes das 06:00
    if hour < 6:
        if not UserBadge.objects.filter(user_profile=profile, badge__slug='early-bird').exists():
            try:
                badge = Badge.objects.get(slug='early-bird')
                UserBadge.objects.create(user_profile=profile, badge=badge)
                new_badges.append(badge)
            except Badge.DoesNotExist:
                pass

    # On Fire - 3 dias de streak
    if profile.current_streak >= 3:
        if not UserBadge.objects.filter(user_profile=profile, badge__slug='on-fire').exists():
            try:
                badge = Badge.objects.get(slug='on-fire')
                UserBadge.objects.create(user_profile=profile, badge=badge)
                new_badges.append(badge)
            except Badge.DoesNotExist:
                pass

    # Consistency King - 30 dias de streak
    if profile.current_streak >= 30:
        if not UserBadge.objects.filter(user_profile=profile, badge__slug='consistency-king').exists():
            try:
                badge = Badge.objects.get(slug='consistency-king')
                UserBadge.objects.create(user_profile=profile, badge=badge)
                new_badges.append(badge)
            except Badge.DoesNotExist:
                pass

    # === BADGES DE HABILIDADE (Skill Tree) ===
    
    # Snake Charmer - 50h em Python
    if session.skill and session.skill.name == 'Python':
        python_minutes = StudySession.objects.filter(
            user=user, 
            skill__name='Python'
        ).aggregate(total=Sum('duration_minutes'))['total'] or 0
        python_hours = python_minutes / 60
        
        if python_hours >= 50:
            if not UserBadge.objects.filter(user_profile=profile, badge__slug='snake-charmer').exists():
                try:
                    badge = Badge.objects.get(slug='snake-charmer')
                    UserBadge.objects.create(user_profile=profile, badge=badge)
                    new_badges.append(badge)
                except Badge.DoesNotExist:
                    pass

    # Code Master - 500h de CODING
    coding_minutes = StudySession.objects.filter(
        user=user, 
        method='CODING'
    ).aggregate(total=Sum('duration_minutes'))['total'] or 0
    coding_hours = coding_minutes / 60
    
    if coding_hours >= 500:
        if not UserBadge.objects.filter(user_profile=profile, badge__slug='code-master').exists():
            try:
                badge = Badge.objects.get(slug='code-master')
                UserBadge.objects.create(user_profile=profile, badge=badge)
                new_badges.append(badge)
            except Badge.DoesNotExist:
                pass

    # === APLICAR RECOMPENSAS ===
    for badge in new_badges:
        profile.current_xp += badge.xp_bonus
        profile.dev_coins += badge.coin_bonus
    
    if new_badges:
        profile.save()
    
    return new_badges


def get_user_badges_progress(user):
    """
    Retorna progresso do usuário em todas as badges
    Útil para mostrar "faltam X horas para desbloquear"
    """
    profile = user.profile
    all_badges = Badge.objects.all()
    unlocked_ids = UserBadge.objects.filter(user_profile=profile).values_list('badge_id', flat=True)
    
    progress = []
    
    for badge in all_badges:
        is_unlocked = badge.id in unlocked_ids
        percentage = 0
        remaining = None
        
        # Calcular progresso baseado no slug
        if not is_unlocked:
            if badge.slug == 'centuriao':
                total_minutes = StudySession.objects.filter(user=user).aggregate(
                    total=Sum('duration_minutes')
                )['total'] or 0
                total_hours = total_minutes / 60
                percentage = min(int((total_hours / 100) * 100), 100)
                remaining = max(0, 100 - total_hours)
            
            elif badge.slug == 'snake-charmer':
                python_minutes = StudySession.objects.filter(
                    user=user, 
                    skill__name='Python'
                ).aggregate(total=Sum('duration_minutes'))['total'] or 0
                python_hours = python_minutes / 60
                percentage = min(int((python_hours / 50) * 100), 100)
                remaining = max(0, 50 - python_hours)
            
            elif badge.slug == 'consistency-king':
                percentage = min(int((profile.current_streak / 30) * 100), 100)
                remaining = max(0, 30 - profile.current_streak)
        
        progress.append({
            'badge': badge,
            'unlocked': is_unlocked,
            'percentage': percentage,
            'remaining': remaining
        })
    
    return progress
