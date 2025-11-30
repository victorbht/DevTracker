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

    # 4. ROTAS GENÉRICAS / DASHBOARD (Prioridade Baixa - Devem ficar por último)
    # O Django lê de cima para baixo. Se esta estivesse em cima,
    # ele acharia que "conquistas" é um nome de período.
    path('<str:periodo>/', views.index, name='index'), 
    path('', views.index, name='index'),
]