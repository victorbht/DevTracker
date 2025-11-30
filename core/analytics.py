"""
Sistema de Analytics Avançado
Fornece insights inteligentes e análise preditiva
"""

from django.db.models import Sum, Count, Avg, F, Q
from django.utils import timezone
from datetime import timedelta, datetime
import json


class AnalyticsEngine:
    """Motor de análise de dados de estudo"""
    
    def __init__(self, user):
        self.user = user
    
    def get_productivity_score(self):
        """
        Calcula score de produtividade (0-100)
        Considera: consistência, volume, variedade de métodos
        """
        from .models import SessaoEstudo
        
        hoje = timezone.now().date()
        mes_inicio = hoje.replace(day=1)
        
        # Dados do mês
        sessoes_mes = SessaoEstudo.objects.filter(
            data_registro__date__gte=mes_inicio
        )
        
        # 1. Consistência (40 pontos) - baseado em streak
        dias_estudados = sessoes_mes.dates('data_registro', 'day').count()
        dias_no_mes = (hoje - mes_inicio).days + 1
        consistencia = min(40, int((dias_estudados / dias_no_mes) * 40))
        
        # 2. Volume (40 pontos) - baseado em horas
        total_horas = sessoes_mes.aggregate(t=Sum('tempo_liquido'))['t']
        horas = total_horas.total_seconds() / 3600 if total_horas else 0
        volume = min(40, int((horas / 40) * 40))  # 40h = pontuação máxima
        
        # 3. Variedade (20 pontos) - diferentes métodos e tecnologias
        metodos_usados = sessoes_mes.values('metodo').distinct().count()
        techs_usadas = sessoes_mes.values('tecnologia').distinct().count()
        variedade = min(20, (metodos_usados * 5) + (techs_usadas * 2))
        
        score_total = consistencia + volume + variedade
        
        return {
            'score': score_total,
            'consistencia': consistencia,
            'volume': volume,
            'variedade': variedade,
            'dias_estudados': dias_estudados,
            'horas_totais': round(horas, 1)
        }
    
    def predict_next_week_hours(self):
        """
        Prevê quantas horas o usuário provavelmente estudará na próxima semana
        Usa média ponderada das últimas 4 semanas (semanas mais recentes têm mais peso)
        """
        from .models import SessaoEstudo
        
        hoje = timezone.now().date()
        horas_por_semana = []
        
        for i in range(4):
            semana_inicio = hoje - timedelta(days=hoje.weekday() + (i * 7))
            semana_fim = semana_inicio + timedelta(days=6)
            horas = SessaoEstudo.objects.filter(
                data_registro__date__gte=semana_inicio,
                data_registro__date__lte=semana_fim
            ).aggregate(t=Sum('tempo_liquido'))['t']
            horas_por_semana.append(horas.total_seconds() / 3600 if horas else 0)
        
        # Média ponderada: semanas recentes têm peso maior
        if horas_por_semana:
            pesos = [4, 3, 2, 1]  # Semana mais recente = peso 4
            media_ponderada = sum(h * p for h, p in zip(horas_por_semana, pesos)) / sum(pesos)
            return round(media_ponderada, 1)
        return 0
    
    def get_best_study_times(self):
        """
        Identifica os melhores horários de estudo do usuário
        """
        from .models import SessaoEstudo
        
        # Agrupa por hora do dia
        sessoes_por_hora = {}
        sessoes = SessaoEstudo.objects.all()
        
        for sessao in sessoes:
            hora = sessao.data_registro.hour
            if hora not in sessoes_por_hora:
                sessoes_por_hora[hora] = {'count': 0, 'total_sec': 0}
            sessoes_por_hora[hora]['count'] += 1
            sessoes_por_hora[hora]['total_sec'] += sessao.tempo_liquido.total_seconds()
        
        # Ordena por frequência
        ranking = sorted(sessoes_por_hora.items(), key=lambda x: x[1]['count'], reverse=True)
        
        periodos = {
            'manha': [],    # 6-12
            'tarde': [],    # 12-18
            'noite': [],    # 18-24
            'madrugada': [] # 0-6
        }
        
        for hora, dados in ranking:
            periodo = 'madrugada'
            if 6 <= hora < 12:
                periodo = 'manha'
            elif 12 <= hora < 18:
                periodo = 'tarde'
            elif 18 <= hora < 24:
                periodo = 'noite'
            
            periodos[periodo].append({
                'hora': hora,
                'sessoes': dados['count'],
                'media_minutos': round(dados['total_sec'] / dados['count'] / 60, 1)
            })
        
        # Identifica período preferido
        periodo_preferido = max(
            [(p, sum(h['sessoes'] for h in horas)) for p, horas in periodos.items()],
            key=lambda x: x[1]
        )[0] if any(periodos.values()) else None
        
        return {
            'periodos': periodos,
            'periodo_preferido': periodo_preferido,
            'top_3_horas': ranking[:3]
        }
    
    def get_technology_mastery(self):
        """
        Calcula nível de maestria em cada tecnologia
        """
        from .models import SessaoEstudo
        
        tech_stats = SessaoEstudo.objects.values('tecnologia__nome').annotate(
            total_horas=Sum('tempo_liquido'),
            total_sessoes=Count('id'),
            total_exercicios=Sum('qtd_exercicios'),
            total_acertos=Sum('qtd_acertos')
        )
        
        maestria = []
        for tech in tech_stats:
            horas = tech['total_horas'].total_seconds() / 3600
            
            # Cálculo de maestria (0-100)
            # Base: horas (max 50 pontos)
            pontos_horas = min(50, int(horas * 2))
            
            # Sessões (consistência - max 25 pontos)
            pontos_sessoes = min(25, tech['total_sessoes'] * 2)
            
            # Taxa de acerto (max 25 pontos)
            taxa_acerto = 0
            if tech['total_exercicios'] and tech['total_exercicios'] > 0:
                taxa_acerto = (tech['total_acertos'] / tech['total_exercicios']) * 100
            pontos_acerto = int(taxa_acerto * 0.25)
            
            maestria_score = pontos_horas + pontos_sessoes + pontos_acerto
            
            # Nível baseado no score
            nivel = 'Iniciante'
            if maestria_score >= 80:
                nivel = 'Mestre'
            elif maestria_score >= 60:
                nivel = 'Avançado'
            elif maestria_score >= 40:
                nivel = 'Intermediário'
            
            maestria.append({
                'tecnologia': tech['tecnologia__nome'],
                'score': maestria_score,
                'nivel': nivel,
                'horas': round(horas, 1),
                'sessoes': tech['total_sessoes'],
                'taxa_acerto': round(taxa_acerto, 1) if tech['total_exercicios'] else None
            })
        
        return sorted(maestria, key=lambda x: x['score'], reverse=True)
    
    def get_study_patterns(self):
        """
        Identifica padrões de estudo
        """
        from .models import SessaoEstudo
        
        hoje = timezone.now().date()
        mes_atras = hoje - timedelta(days=30)
        
        sessoes = SessaoEstudo.objects.filter(
            data_registro__date__gte=mes_atras
        )
        
        # Padrão de duração
        duracoes = [s.tempo_liquido.total_seconds() / 60 for s in sessoes]
        duracao_media = sum(duracoes) / len(duracoes) if duracoes else 0
        
        # Sessões longas vs curtas
        sessoes_longas = sum(1 for d in duracoes if d > 60)  # > 1h
        sessoes_curtas = sum(1 for d in duracoes if d <= 30)  # <= 30min
        
        # Dias da semana preferidos
        por_dia_semana = {}
        dias_nome = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        
        for sessao in sessoes:
            dia = sessao.data_registro.weekday()
            por_dia_semana[dia] = por_dia_semana.get(dia, 0) + 1
        
        dia_favorito = max(por_dia_semana.items(), key=lambda x: x[1])[0] if por_dia_semana else None
        
        return {
            'duracao_media': round(duracao_media, 1),
            'preferencia_duracao': 'longas' if sessoes_longas > sessoes_curtas else 'curtas',
            'sessoes_longas': sessoes_longas,
            'sessoes_curtas': sessoes_curtas,
            'dia_favorito': dias_nome[dia_favorito] if dia_favorito is not None else None,
            'distribuicao_semanal': {dias_nome[k]: v for k, v in sorted(por_dia_semana.items())}
        }
    
    def get_achievement_prediction(self):
        """
        Prevê próximas conquistas alcançáveis
        """
        from .models import Conquista, SessaoEstudo, PerfilUsuario
        from .cache_utils import get_user_total_hours, get_user_streak
        
        perfil = PerfilUsuario.objects.get(user=self.user)
        total_horas = get_user_total_hours(self.user)
        streak_atual = get_user_streak(self.user)
        
        # Conquistas não alcançadas
        nao_alcancadas = Conquista.objects.exclude(
            id__in=perfil.conquistas.values_list('id', flat=True)
        )
        
        proximas = []
        for conquista in nao_alcancadas:
            progresso = 0
            tempo_estimado = None
            
            if conquista.categoria == 'tempo':
                progresso = (total_horas / conquista.quantidade_necessaria) * 100
                faltam = conquista.quantidade_necessaria - total_horas
                # Estima baseado na média semanal
                predicao = self.predict_next_week_hours()
                if predicao > 0:
                    semanas = faltam / predicao
                    tempo_estimado = f"{int(semanas)} semanas"
            
            elif conquista.categoria == 'streak':
                progresso = (streak_atual / conquista.quantidade_necessaria) * 100
                faltam = conquista.quantidade_necessaria - streak_atual
                tempo_estimado = f"{int(faltam)} dias"
            
            if progresso > 0:
                proximas.append({
                    'conquista': conquista,
                    'progresso': min(100, round(progresso, 1)),
                    'tempo_estimado': tempo_estimado
                })
        
        # Ordena por proximidade
        return sorted(proximas, key=lambda x: x['progresso'], reverse=True)[:5]


def generate_weekly_report(user):
    """
    Gera relatório semanal completo
    """
    analytics = AnalyticsEngine(user)
    
    return {
        'productivity_score': analytics.get_productivity_score(),
        'prediction': analytics.predict_next_week_hours(),
        'best_times': analytics.get_best_study_times(),
        'patterns': analytics.get_study_patterns(),
        'next_achievements': analytics.get_achievement_prediction(),
        'technology_mastery': analytics.get_technology_mastery()
    }
