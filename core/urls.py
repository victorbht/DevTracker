from django.urls import path
from . import views, views_advanced

app_name = 'core'

urlpatterns = [
    # 1. ROTAS ESPECÍFICAS (Prioridade Alta - Devem vir primeiro)
    # Rota temporária para criar badges (Execute e depois pode remover)
    path('setup-badges/', views.popular_badges, name='popular_badges'),
    
    # Rota da Galeria de Conquistas
    path('conquistas/', views.galeria_conquistas, name='conquistas'),
    
    # Rota de Estatísticas
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    
    # === NOVAS FUNCIONALIDADES AVANÇADAS ===
    # Rankings e Leaderboards
    path('rankings/', views_advanced.leaderboards_view, name='rankings'),
    path('rankings/compare/<str:username>/', views_advanced.compare_achievements, name='compare_achievements'),
    path('rankings/rarest/', views_advanced.rarest_achievements, name='rarest_achievements'),
    
    # Analytics Avançado
    path('analytics/', views_advanced.analytics_dashboard, name='analytics'),
    path('analytics/weekly-report/', views_advanced.weekly_report_view, name='weekly_report'),
    
    # Export/Import
    path('export/', views_advanced.export_data, name='export_data'),
    path('import/', views_advanced.import_data, name='import_data'),
    
    # APIs JSON
    path('api/stats/', views_advanced.api_user_stats, name='api_stats'),
    path('api/productivity/', views_advanced.api_productivity_score, name='api_productivity'),
    path('api/ranking/', views_advanced.api_global_ranking, name='api_ranking'),
    path('api/my-position/', views_advanced.api_my_position, name='api_my_position'),
    
    # Cache Management
    path('cache/warm/', views_advanced.warm_cache, name='warm_cache'),
    path('cache/clear/', views_advanced.clear_cache, name='clear_cache'),
    
    # PACOTE GAMER
    path('gamer/', views.dashboard_gamer, name='dashboard_gamer'),
    path('gamer/quests/', views.quest_board, name='quest_board'),
    path('gamer/arena/<int:boss_id>/', views.battle_arena, name='battle_arena'),
    path('gamer/inventario/', views.inventario, name='inventario'),
    path('gamer/session/create/', views.create_session, name='create_session'),
    path('gamer/skill-tree/', views.skill_tree, name='skill_tree'),
    path('gamer/roadmap/', views.skill_tree, name='roadmap'),
    path('gamer/conquistas/', views.conquistas_rpg, name='conquistas_rpg'),
    path('gamer/profile/', views.user_profile, name='user_profile'),
    path('gamer/trophies/', views.trophy_room, name='trophy_room'),
    
    # Alias para dashboards
    path('dashboard/', views.index, name='dashboard_classico'),
    path('dashboard/rpg/', views.dashboard_gamer, name='dashboard'),
    
    # 2. ROTAS DE GERENCIAMENTO (Configurações)
    path('tech/salvar/', views.salvar_tech, name='salvar_tech'),
    path('tech/excluir/<int:id>/', views.excluir_tech, name='excluir_tech'),
    path('metodo/salvar/', views.salvar_metodo, name='salvar_metodo'),
    path('metodo/excluir/<int:id>/', views.excluir_metodo, name='excluir_metodo'),
    path('metas/salvar/', views.salvar_metas, name='salvar_metas'),

    # 3. ROTAS DE CRUD SESSÃO (Com ID)
    path('editar/<int:id>/', views.editar_sessao, name='editar'),
    path('editar-tempo/<int:id>/', views.editar_tempo, name='editar_tempo'),
    path('excluir/<int:id>/', views.excluir_sessao, name='excluir'),

    # 4. ROTAS GENÉRICAS / DASHBOARD (Prioridade Baixa)
    path('<str:periodo>/', views.index, name='index_periodo'), 
    path('', views.index, name='index'),
]