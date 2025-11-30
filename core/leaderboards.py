"""
Sistema de Ranking e Leaderboards
Rankings globais, por categoria e competições
"""

from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache


class LeaderboardManager:
    """Gerenciador de rankings e leaderboards"""
    
    CACHE_TIMEOUT = 300  # 5 minutos
    
    @staticmethod
    def get_global_ranking(limit=50, period='all'):
        """
        Ranking global por XP total
        period: 'all', 'month', 'week'
        """
        cache_key = f'ranking_global_{period}_{limit}'
        ranking = cache.get(cache_key)
        
        if ranking is None:
            from .models import PerfilUsuario
            from django.contrib.auth.models import User
            
            perfis = PerfilUsuario.objects.select_related('user').only(
                'user__username', 'user__date_joined', 'xp_total', 'nivel'
            )
            
            # Filtro por período (se necessário, adicionar campo timestamp em conquistas)
            # Por enquanto usa xp_total que é acumulativo
            
            ranking = []
            for idx, perfil in enumerate(perfis.order_by('-xp_total')[:limit]):
                ranking.append({
                    'posicao': idx + 1,
                    'username': perfil.user.username,
                    'xp': perfil.xp_total,
                    'nivel': perfil.nivel,
                    'badge_count': perfil.conquistas.count()
                })
            
            cache.set(cache_key, ranking, LeaderboardManager.CACHE_TIMEOUT)
        
        return ranking
    
    @staticmethod
    def get_technology_ranking(tech_name, limit=30):
        """Ranking por tecnologia específica"""
        cache_key = f'ranking_tech_{tech_name}_{limit}'
        ranking = cache.get(cache_key)
        
        if ranking is None:
            from .models import SessaoEstudo, Tecnologia
            from django.contrib.auth.models import User
            
            try:
                tech = Tecnologia.objects.get(nome=tech_name)
            except Tecnologia.DoesNotExist:
                return []
            
            # Agrupa por usuário (precisa adicionar user FK em SessaoEstudo)
            # Por enquanto retorna stats gerais
            ranking = []
            cache.set(cache_key, ranking, LeaderboardManager.CACHE_TIMEOUT)
        
        return ranking
    
    @staticmethod
    def get_streak_ranking(limit=30):
        """Ranking por streak atual"""
        cache_key = f'ranking_streak_{limit}'
        ranking = cache.get(cache_key)
        
        if ranking is None:
            from .models import UserProfile
            
            perfis = UserProfile.objects.select_related('user').only(
                'user__username', 'current_streak', 'longest_streak', 'level'
            ).filter(current_streak__gt=0).order_by('-current_streak')[:limit]
            
            ranking = [
                {
                    'posicao': idx + 1,
                    'username': p.user.username,
                    'streak_atual': p.current_streak,
                    'streak_record': p.longest_streak,
                    'nivel': p.level
                }
                for idx, p in enumerate(perfis)
            ]
            
            cache.set(cache_key, ranking, LeaderboardManager.CACHE_TIMEOUT)
        
        return ranking
    
    @staticmethod
    def get_weekly_competition():
        """
        Competição semanal - quem estudou mais esta semana
        """
        cache_key = 'weekly_competition'
        competition = cache.get(cache_key)
        
        if competition is None:
            from .models import SessaoEstudo
            
            hoje = timezone.now().date()
            semana_inicio = hoje - timedelta(days=hoje.weekday())
            
            # Precisa adicionar FK de user em SessaoEstudo
            # Por enquanto retorna estrutura vazia
            competition = {
                'inicio': semana_inicio,
                'fim': semana_inicio + timedelta(days=6),
                'participantes': [],
                'total_horas': 0
            }
            
            cache.set(cache_key, competition, LeaderboardManager.CACHE_TIMEOUT)
        
        return competition
    
    @staticmethod
    def get_user_position(user):
        """Retorna posição do usuário nos rankings"""
        positions = {}
        
        # Posição global
        global_ranking = LeaderboardManager.get_global_ranking(limit=1000)
        for idx, entry in enumerate(global_ranking):
            if entry['username'] == user.username:
                positions['global'] = idx + 1
                break
        
        # Posição streak
        streak_ranking = LeaderboardManager.get_streak_ranking(limit=1000)
        for idx, entry in enumerate(streak_ranking):
            if entry['username'] == user.username:
                positions['streak'] = idx + 1
                break
        
        return positions
    
    @staticmethod
    def get_nearby_competitors(user, range_size=5):
        """
        Retorna competidores próximos ao usuário no ranking
        """
        positions = LeaderboardManager.get_user_position(user)
        global_pos = positions.get('global', 0)
        
        if global_pos == 0:
            return []
        
        # Pega ranking completo e filtra ao redor da posição
        full_ranking = LeaderboardManager.get_global_ranking(limit=1000)
        
        start = max(0, global_pos - range_size - 1)
        end = min(len(full_ranking), global_pos + range_size)
        
        return full_ranking[start:end]


class AchievementComparison:
    """Compara conquistas entre usuários"""
    
    @staticmethod
    def compare_with_user(user1, user2):
        """Compara conquistas de dois usuários"""
        from .models import PerfilUsuario
        
        try:
            perfil1 = PerfilUsuario.objects.get(user=user1)
            perfil2 = PerfilUsuario.objects.get(user=user2)
        except PerfilUsuario.DoesNotExist:
            return None
        
        conquistas1 = set(perfil1.conquistas.values_list('id', flat=True))
        conquistas2 = set(perfil2.conquistas.values_list('id', flat=True))
        
        return {
            'user1': {
                'total': len(conquistas1),
                'exclusivas': len(conquistas1 - conquistas2),
                'xp': perfil1.xp_total,
                'nivel': perfil1.nivel
            },
            'user2': {
                'total': len(conquistas2),
                'exclusivas': len(conquistas2 - conquistas1),
                'xp': perfil2.xp_total,
                'nivel': perfil2.nivel
            },
            'em_comum': len(conquistas1 & conquistas2)
        }
    
    @staticmethod
    def get_rarest_achievements(user, limit=5):
        """Conquistas mais raras do usuário"""
        from .models import PerfilUsuario
        
        try:
            perfil = PerfilUsuario.objects.get(user=user)
        except PerfilUsuario.DoesNotExist:
            return []
        
        # Conta quantos usuários têm cada conquista
        minhas_conquistas = perfil.conquistas.all()
        
        raridade = []
        total_users = PerfilUsuario.objects.count()
        
        for conquista in minhas_conquistas:
            usuarios_com = PerfilUsuario.objects.filter(conquistas=conquista).count()
            pct_raridade = (usuarios_com / total_users) * 100 if total_users > 0 else 0
            
            raridade.append({
                'conquista': conquista,
                'usuarios': usuarios_com,
                'raridade_pct': round(pct_raridade, 2),
                'nivel_raridade': 'Lendária' if pct_raridade < 5 else 'Épica' if pct_raridade < 15 else 'Rara'
            })
        
        return sorted(raridade, key=lambda x: x['raridade_pct'])[:limit]


def get_leaderboard_context(user):
    """
    Retorna contexto completo de leaderboards para templates
    """
    manager = LeaderboardManager()
    
    return {
        'global_top_10': manager.get_global_ranking(limit=10),
        'streak_top_10': manager.get_streak_ranking(limit=10),
        'my_positions': manager.get_user_position(user),
        'nearby_competitors': manager.get_nearby_competitors(user, range_size=3),
        'weekly_competition': manager.get_weekly_competition(),
        'rarest_achievements': AchievementComparison.get_rarest_achievements(user)
    }
