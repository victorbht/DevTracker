"""
Sistema de Cache Inteligente para DevTracker
Otimiza queries frequentes e reduz carga no banco de dados
"""

from django.core.cache import cache
from django.db.models import Sum, Count, Avg
from datetime import timedelta
from django.utils import timezone
from functools import wraps


# Tempos de cache em segundos
CACHE_SHORT = 60  # 1 minuto
CACHE_MEDIUM = 300  # 5 minutos
CACHE_LONG = 1800  # 30 minutos
CACHE_VERY_LONG = 3600  # 1 hora


def cache_user_stats(timeout=CACHE_MEDIUM):
    """
    Decorator para cachear estatísticas do usuário
    """
    def decorator(func):
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            cache_key = f'user_stats_{user.id}_{func.__name__}'
            result = cache.get(cache_key)
            if result is None:
                result = func(user, *args, **kwargs)
                cache.set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator


def invalidate_user_cache(user):
    """
    Invalida todo o cache relacionado ao usuário
    Chamar após criar/editar/deletar sessões
    """
    from django.core.cache import cache
    # Limpa padrões de cache do usuário
    cache.delete_pattern(f'user_stats_{user.id}_*')
    cache.delete(f'user_conquistas_{user.id}')
    cache.delete(f'user_ranking_{user.id}')


@cache_user_stats(timeout=CACHE_MEDIUM)
def get_user_total_hours(user):
    """Retorna total de horas de estudo do usuário (cached)"""
    from .models import SessaoEstudo
    total = SessaoEstudo.objects.aggregate(t=Sum('tempo_liquido'))['t']
    return total.total_seconds() / 3600 if total else 0


@cache_user_stats(timeout=CACHE_MEDIUM)
def get_user_streak(user):
    """Calcula streak atual do usuário (cached)"""
    from .models import SessaoEstudo
    datas = list(SessaoEstudo.objects.dates('data_registro', 'day').order_by('-data_registro'))
    streak = 0
    hoje = timezone.now().date()
    
    if datas and (datas[0] == hoje or datas[0] == hoje - timedelta(days=1)):
        check = datas[0]
        for d in datas:
            if d == check:
                streak += 1
                check -= timedelta(days=1)
            else:
                break
    return streak


@cache_user_stats(timeout=CACHE_LONG)
def get_tech_distribution(user):
    """Distribuição de horas por tecnologia (cached)"""
    from .models import SessaoEstudo
    return list(SessaoEstudo.objects.values('tecnologia__nome').annotate(
        total=Sum('tempo_liquido'),
        count=Count('id')
    ).order_by('-total'))


@cache_user_stats(timeout=CACHE_LONG)
def get_method_distribution(user):
    """Distribuição de horas por método (cached)"""
    from .models import SessaoEstudo
    return list(SessaoEstudo.objects.values('metodo__nome').annotate(
        total=Sum('tempo_liquido'),
        count=Count('id')
    ).order_by('-total'))


def get_global_ranking(limit=100, cache_timeout=CACHE_LONG):
    """
    Ranking global de usuários
    Cache por 30 minutos para evitar sobrecarga
    """
    cache_key = f'global_ranking_{limit}'
    ranking = cache.get(cache_key)
    
    if ranking is None:
        from .models import PerfilUsuario
        from django.contrib.auth.models import User
        
        # Query otimizada
        ranking = PerfilUsuario.objects.select_related('user').only(
            'user__username', 'xp_total', 'nivel'
        ).order_by('-xp_total')[:limit]
        
        ranking = [
            {
                'username': p.user.username,
                'xp_total': p.xp_total,
                'nivel': p.nivel,
                'posicao': idx + 1
            }
            for idx, p in enumerate(ranking)
        ]
        cache.set(cache_key, ranking, cache_timeout)
    
    return ranking


def get_weekly_insights(user, cache_timeout=CACHE_MEDIUM):
    """
    Insights da semana: comparação com semana anterior, melhor dia, etc
    """
    cache_key = f'weekly_insights_{user.id}'
    insights = cache.get(cache_key)
    
    if insights is None:
        from .models import SessaoEstudo
        hoje = timezone.now().date()
        semana_inicio = hoje - timedelta(days=hoje.weekday())
        semana_passada_inicio = semana_inicio - timedelta(days=7)
        
        # Semana atual
        horas_semana_atual = SessaoEstudo.objects.filter(
            data_registro__date__gte=semana_inicio
        ).aggregate(t=Sum('tempo_liquido'))['t']
        horas_atual = horas_semana_atual.total_seconds() / 3600 if horas_semana_atual else 0
        
        # Semana passada
        horas_semana_passada = SessaoEstudo.objects.filter(
            data_registro__date__gte=semana_passada_inicio,
            data_registro__date__lt=semana_inicio
        ).aggregate(t=Sum('tempo_liquido'))['t']
        horas_passada = horas_semana_passada.total_seconds() / 3600 if horas_semana_passada else 0
        
        # Melhor dia da semana
        por_dia = SessaoEstudo.objects.filter(
            data_registro__date__gte=semana_inicio
        ).values('data_registro__date').annotate(
            total=Sum('tempo_liquido')
        ).order_by('-total')
        
        melhor_dia = None
        if por_dia:
            melhor_dia = {
                'data': por_dia[0]['data_registro__date'],
                'horas': por_dia[0]['total'].total_seconds() / 3600
            }
        
        insights = {
            'horas_atual': round(horas_atual, 1),
            'horas_passada': round(horas_passada, 1),
            'diferenca': round(horas_atual - horas_passada, 1),
            'crescimento_pct': round(((horas_atual - horas_passada) / horas_passada * 100), 1) if horas_passada > 0 else 0,
            'melhor_dia': melhor_dia
        }
        
        cache.set(cache_key, insights, cache_timeout)
    
    return insights


def get_recommended_goals(user):
    """
    Recomenda metas personalizadas baseadas no histórico
    """
    cache_key = f'recommended_goals_{user.id}'
    goals = cache.get(cache_key)
    
    if goals is None:
        from .models import SessaoEstudo
        
        # Média das últimas 4 semanas
        hoje = timezone.now().date()
        quatro_semanas_atras = hoje - timedelta(days=28)
        
        horas_por_semana = []
        for i in range(4):
            semana_inicio = hoje - timedelta(days=hoje.weekday() + (i * 7))
            semana_fim = semana_inicio + timedelta(days=6)
            horas = SessaoEstudo.objects.filter(
                data_registro__date__gte=semana_inicio,
                data_registro__date__lte=semana_fim
            ).aggregate(t=Sum('tempo_liquido'))['t']
            horas_por_semana.append(horas.total_seconds() / 3600 if horas else 0)
        
        media_semanal = sum(horas_por_semana) / len(horas_por_semana) if horas_por_semana else 0
        
        # Recomenda 10% a mais que a média
        meta_semanal_recomendada = int(media_semanal * 1.1)
        meta_mensal_recomendada = meta_semanal_recomendada * 4
        
        goals = {
            'semanal': max(meta_semanal_recomendada, 5),  # Mínimo 5h
            'mensal': max(meta_mensal_recomendada, 20),   # Mínimo 20h
            'media_atual': round(media_semanal, 1)
        }
        
        cache.set(cache_key, goals, CACHE_VERY_LONG)
    
    return goals


class CacheManager:
    """
    Gerenciador centralizado de cache
    """
    
    @staticmethod
    def warm_up_user_cache(user):
        """
        Pré-aquece o cache do usuário com dados frequentes
        Chamar após login ou em background task
        """
        get_user_total_hours(user)
        get_user_streak(user)
        get_tech_distribution(user)
        get_method_distribution(user)
        get_weekly_insights(user)
        get_recommended_goals(user)
    
    @staticmethod
    def clear_all_user_cache(user):
        """Limpa todo cache do usuário"""
        invalidate_user_cache(user)
    
    @staticmethod
    def warm_up_global_cache():
        """
        Pré-aquece caches globais
        Executar em task agendada (Celery/cron)
        """
        get_global_ranking(limit=100)
