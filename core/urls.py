from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # 1. ROTAS ESPECÍFICAS (Prioridade Alta - Devem vir primeiro)
    # Rota temporária para criar badges (Execute e depois pode remover)
    path('setup-badges/', views.popular_badges, name='popular_badges'),
    
    # Rota da Galeria de Conquistas
    path('conquistas/', views.galeria_conquistas, name='conquistas'),
    
    # Rota de Estatísticas
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    
    # PACOTE GAMER
    path('gamer/', views.dashboard_gamer, name='dashboard_gamer'),
    path('gamer/quests/', views.quest_board, name='quest_board'),
    path('gamer/arena/<int:boss_id>/', views.battle_arena, name='battle_arena'),
    path('gamer/inventario/', views.inventario, name='inventario'),
    path('gamer/session/create/', views.create_session, name='create_session'),
    path('gamer/skill-tree/', views.skill_tree, name='skill_tree'),
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