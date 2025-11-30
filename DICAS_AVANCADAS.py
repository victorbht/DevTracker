"""
🎯 DICAS AVANÇADAS DE USO - DEVTRACKER 2.0

Este arquivo contém dicas e truques para aproveitar ao máximo
as novas funcionalidades implementadas.
"""

# ============================================
# 1. CACHE INTELIGENTE
# ============================================

from core.cache_utils import *

# Dica 1: Pré-aquecer cache após login
def custom_login_view(request):
    # ... lógica de login ...
    if user.is_authenticated:
        CacheManager.warm_up_user_cache(user)
    # Isso deixa o dashboard super rápido!

# Dica 2: Invalidar cache após operações importantes
def criar_sessao_custom(request):
    # ... criar sessão ...
    invalidate_user_cache(request.user)
    # Cache será recalculado na próxima requisição

# Dica 3: Cache de queries customizadas
@cache_user_stats(timeout=600)  # 10 minutos
def minha_query_pesada(user):
    # Qualquer query complexa aqui
    return resultado

# ============================================
# 2. ANALYTICS PODEROSO
# ============================================

from core.analytics import AnalyticsEngine

# Dica 4: Relatório completo em uma linha
def dashboard_super_completo(request):
    analytics = AnalyticsEngine(request.user)
    
    context = {
        'score': analytics.get_productivity_score(),
        'predicao': analytics.predict_next_week_hours(),
        'horarios': analytics.get_best_study_times(),
        'maestria': analytics.get_technology_mastery(),
        'padroes': analytics.get_study_patterns(),
        'proximas': analytics.get_achievement_prediction()
    }
    
    return render(request, 'dashboard_completo.html', context)

# Dica 5: Recomendações personalizadas
def sugerir_proximo_estudo(user):
    analytics = AnalyticsEngine(user)
    
    # Melhor horário
    horarios = analytics.get_best_study_times()
    melhor_periodo = horarios['periodo_preferido']
    
    # Tecnologia com menor maestria
    maestria = analytics.get_technology_mastery()
    precisa_melhorar = sorted(maestria, key=lambda x: x['score'])[0]
    
    return {
        'quando': f"Estude no período da {melhor_periodo}",
        'o_que': f"Foque em {precisa_melhorar['tecnologia']}"
    }

# Dica 6: Sistema de conquistas inteligente
def verificar_conquistas_personalizadas(user):
    analytics = AnalyticsEngine(user)
    proximas = analytics.get_achievement_prediction()
    
    # Notificar usuário sobre conquistas próximas (>80% progresso)
    iminentes = [c for c in proximas if c['progresso'] > 80]
    
    if iminentes:
        # Enviar notificação/email
        pass

# ============================================
# 3. RANKINGS & GAMIFICAÇÃO
# ============================================

from core.leaderboards import *

# Dica 7: Sistema de recompensas por posição no ranking
def dar_bonus_por_ranking(user):
    positions = LeaderboardManager.get_user_position(user)
    global_pos = positions.get('global', 999)
    
    bonus_coins = 0
    if global_pos == 1:
        bonus_coins = 1000  # Rei do ranking!
    elif global_pos <= 3:
        bonus_coins = 500   # Top 3
    elif global_pos <= 10:
        bonus_coins = 250   # Top 10
    elif global_pos <= 50:
        bonus_coins = 100   # Top 50
    
    if bonus_coins:
        # Adicionar coins ao perfil
        pass

# Dica 8: Rivalidades automáticas
def sugerir_rivalidades(user):
    competidores = LeaderboardManager.get_nearby_competitors(user, range_size=2)
    
    # Pegar usuário logo acima e logo abaixo
    minha_pos = LeaderboardManager.get_user_position(user)['global']
    
    acima = [c for c in competidores if c['posicao'] < minha_pos]
    abaixo = [c for c in competidores if c['posicao'] > minha_pos]
    
    return {
        'desafio': acima[0] if acima else None,      # Usuário para ultrapassar
        'ameaca': abaixo[0] if abaixo else None       # Usuário que pode te ultrapassar
    }

# Dica 9: Conquistas raras como troféus
def sistema_trofeus(user):
    raras = AchievementComparison.get_rarest_achievements(user, limit=20)
    
    lendarias = [r for r in raras if r['nivel_raridade'] == 'Lendária']
    epicas = [r for r in raras if r['nivel_raridade'] == 'Épica']
    
    # Exibir em vitrine especial
    return {
        'lendarias': lendarias,  # Medalhas de ouro
        'epicas': epicas,        # Medalhas de prata
        'score_raridade': len(lendarias) * 100 + len(epicas) * 50
    }

# ============================================
# 4. EXPORT/IMPORT AVANÇADO
# ============================================

from core.export_import import *

# Dica 10: Backup automático semanal
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        from django.contrib.auth.models import User
        
        for user in User.objects.all():
            exporter = DataExporter(user)
            
            # Salvar em arquivo
            with open(f'backups/{user.username}.json', 'w') as f:
                response = exporter.export_achievements_json()
                f.write(response.content.decode())

# Dica 11: Migração de outra plataforma
def importar_de_plataforma_externa(csv_path, user):
    """
    CSV deve ter formato:
    Data, Tecnologia, Tópico, Método, Tempo (HH:MM:SS)
    """
    with open(csv_path, 'rb') as f:
        results = DataImporter.import_sessions_from_csv(f, user)
        
    print(f"Importadas: {results['imported']}")
    print(f"Erros: {results['skipped']}")
    
    if results['errors']:
        for erro in results['errors']:
            print(f"  - {erro}")

# Dica 12: Relatórios customizados
class CustomExporter(DataExporter):
    def export_monthly_report(self, year, month):
        """Relatório mensal específico"""
        from datetime import date
        
        start = date(year, month, 1)
        if month == 12:
            end = date(year + 1, 1, 1)
        else:
            end = date(year, month + 1, 1)
        
        return self.export_sessions_csv(start_date=start, end_date=end)

# ============================================
# 5. TOAST NOTIFICATIONS CRIATIVAS
# ============================================

# Dica 13: Notificações contextuais
"""
JavaScript para adicionar em seus templates:

// Quando completar meta
if (horasEstudadas >= metaSemanal) {
    toastAchievement("Meta Semanal Completa! 🎯", metaSemanal * 10);
}

// Quando quebrar recorde pessoal
if (novaDuracao > recordePessoal) {
    toast.show("🔥 Novo Recorde Pessoal!", "levelup", 8000);
}

// Série de conquistas (combo)
let comboCount = 3;
setTimeout(() => toastAchievement("Primeira", 100), 0);
setTimeout(() => toastAchievement("Segunda", 100), 1000);
setTimeout(() => toastAchievement("Terceira", 100), 2000);
setTimeout(() => toast.show(`🎊 COMBO x${comboCount}!`, "achievement", 5000), 3000);
"""

# Dica 14: Integração com Django Messages
"""
Em suas views:

from django.contrib import messages

def minha_view(request):
    messages.success(request, "Operação concluída!")
    messages.warning(request, "Atenção: Cache será limpo")
    
    # Toast converte automaticamente!
    return redirect('dashboard')
"""

# ============================================
# 6. APIS REST AVANÇADAS
# ============================================

# Dica 15: Dashboard em React/Vue
"""
// Exemplo em JavaScript
async function loadDashboardData() {
    const stats = await fetch('/api/stats/').then(r => r.json());
    const productivity = await fetch('/api/productivity/').then(r => r.json());
    const ranking = await fetch('/api/ranking/?limit=10').then(r => r.json());
    
    return { stats, productivity, ranking };
}
"""

# Dica 16: Webhook para integrações
def webhook_new_achievement(user, conquista):
    """Notificar serviços externos"""
    import requests
    
    payload = {
        'user': user.username,
        'achievement': conquista.nome,
        'xp': conquista.xp_reward,
        'timestamp': timezone.now().isoformat()
    }
    
    # Enviar para Discord, Slack, etc
    requests.post('https://hooks.slack.com/...', json=payload)

# Dica 17: GraphQL (avançado)
"""
Para implementar GraphQL:

pip install graphene-django

# Em schema.py:
import graphene
from graphene_django import DjangoObjectType

class UserStatsType(graphene.ObjectType):
    username = graphene.String()
    xp = graphene.Int()
    nivel = graphene.Int()

class Query(graphene.ObjectType):
    my_stats = graphene.Field(UserStatsType)
    
    def resolve_my_stats(self, info):
        user = info.context.user
        perfil = PerfilUsuario.objects.get(user=user)
        return {
            'username': user.username,
            'xp': perfil.xp_total,
            'nivel': perfil.nivel
        }

schema = graphene.Schema(query=Query)
"""

# ============================================
# 7. PERFORMANCE EXTREMA
# ============================================

# Dica 18: Paginação eficiente
from django.core.paginator import Paginator

def lista_otimizada(request):
    queryset = SessaoEstudo.objects.select_related(
        'tecnologia', 'metodo'
    ).only(
        'id', 'tecnologia__nome', 'topico', 'tempo_liquido'
    )
    
    paginator = Paginator(queryset, 50)  # 50 por página
    page = paginator.get_page(request.GET.get('page', 1))
    
    # Resultado: apenas 1 query!
    return render(request, 'lista.html', {'page': page})

# Dica 19: Aggregations em cache
@cache_user_stats(timeout=3600)  # 1 hora
def estatisticas_pesadas(user):
    from django.db.models import Avg, Max, Min, StdDev
    
    stats = SessaoEstudo.objects.aggregate(
        media=Avg('tempo_liquido'),
        maximo=Max('tempo_liquido'),
        minimo=Min('tempo_liquido'),
        desvio=StdDev('qtd_acertos')
    )
    
    return stats

# Dica 20: Batch operations
def processar_em_lote(users):
    """Processar múltiplos usuários eficientemente"""
    from django.db.models import Prefetch
    
    # Carregar tudo de uma vez
    users = User.objects.prefetch_related(
        Prefetch('perfil__conquistas'),
        Prefetch('profile__badges'),
        Prefetch('profile__skills_desbloqueadas')
    )
    
    for user in users:
        # Processa sem queries adicionais
        pass

# ============================================
# 8. GAMIFICAÇÃO AVANÇADA
# ============================================

# Dica 21: Eventos temporários
def evento_double_xp():
    """Durante finais de semana, XP em dobro"""
    from datetime import datetime
    
    hoje = datetime.now()
    if hoje.weekday() in [5, 6]:  # Sábado ou Domingo
        return 2.0  # Multiplicador
    return 1.0

def registrar_sessao_com_bonus(sessao, user):
    multiplicador = evento_double_xp()
    xp_base = calcular_xp(sessao)
    xp_final = int(xp_base * multiplicador)
    
    if multiplicador > 1:
        toast.show(f"🎉 Evento Double XP! {xp_final} XP ganhos", "achievement")

# Dica 22: Conquistas em cadeia
def verificar_conquista_em_cadeia(user, conquista_desbloqueada):
    """Quando desbloquear conquista X, verifica se desbloqueou Y"""
    
    # Ex: "10 horas Python" + "10 horas Django" = "Full Stack Python"
    perfil = PerfilUsuario.objects.get(user=user)
    conquistas = set(perfil.conquistas.values_list('slug', flat=True))
    
    combos = {
        frozenset(['python-10h', 'django-10h']): 'fullstack-python',
        frozenset(['react-10h', 'node-10h']): 'fullstack-javascript',
    }
    
    for required, unlock in combos.items():
        if required.issubset(conquistas):
            # Desbloquear conquista especial!
            pass

# Dica 23: Títulos dinâmicos
def calcular_titulo_atual(user):
    """Título muda baseado em conquistas"""
    perfil = PerfilUsuario.objects.get(user=user)
    raras = AchievementComparison.get_rarest_achievements(user)
    
    lendarias = sum(1 for r in raras if r['nivel_raridade'] == 'Lendária')
    
    if lendarias >= 5:
        return "🌟 Lenda Viva"
    elif perfil.nivel >= 100:
        return "👑 Grão-Mestre"
    elif perfil.nivel >= 50:
        return "⚔️ Mestre"
    else:
        return "🎯 Desenvolvedor"

# ============================================
# 9. MACHINE LEARNING (FUTURO)
# ============================================

# Dica 24: Previsão com ML
"""
Futuramente, adicionar scikit-learn:

from sklearn.linear_model import LinearRegression
import numpy as np

def prever_horas_proxima_semana(user):
    # Pegar histórico das últimas 12 semanas
    historico = get_weekly_hours(user, weeks=12)
    
    X = np.array(range(len(historico))).reshape(-1, 1)
    y = np.array(historico)
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Prever semana 13
    predicao = model.predict([[12]])[0]
    
    return max(0, predicao)  # Não pode ser negativo
"""

# ============================================
# 10. MONITORAMENTO & LOGS
# ============================================

# Dica 25: Logging estruturado
import logging

logger = logging.getLogger(__name__)

def acao_importante(user, acao):
    logger.info(f"User {user.username} executou {acao}", extra={
        'user_id': user.id,
        'acao': acao,
        'timestamp': timezone.now().isoformat()
    })

# Dica 26: Métricas customizadas
from django.db.models.signals import post_save

@receiver(post_save, sender=SessaoEstudo)
def track_session_created(sender, instance, created, **kwargs):
    if created:
        # Incrementar contador no cache
        cache_key = f'sessions_today_{timezone.now().date()}'
        cache.incr(cache_key, 1)
        
        # Se for a sessão 1000 do dia
        if cache.get(cache_key) == 1000:
            # Notificar administradores
            pass

"""
🎉 FIM DAS DICAS AVANÇADAS

Estas são apenas algumas ideias para expandir o sistema.
Use sua criatividade para criar funcionalidades únicas!

Próximos passos sugeridos:
1. Implementar sistema de badges customizáveis
2. Criar desafios/quests diários
3. Adicionar sistema de mentoria
4. Integrar com plataformas de código (GitHub, GitLab)
5. Criar app mobile com React Native

Boa sorte! 🚀
"""
