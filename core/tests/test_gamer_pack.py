import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from core.models import (
    SkillNode, PerfilGamer, SessaoGamer, ItemLoja, InventarioUsuario,
    QuestEmprego, BossBattle, SubmissaoProjeto, CodeReview
)

@pytest.mark.django_db
class TestSkillNode:
    def test_criar_skill_node(self):
        skill = SkillNode.objects.create(nome="Python", icone_fa="fab fa-python")
        assert skill.slug == "python"
        assert str(skill) == "Python"
    
    def test_skill_tree_hierarquia(self):
        python = SkillNode.objects.create(nome="Python")
        django = SkillNode.objects.create(nome="Django", parent=python)
        
        assert django.parent == python
        assert django in python.children.all()

@pytest.mark.django_db
class TestPerfilGamer:
    def test_criar_perfil_automatico(self):
        user = User.objects.create_user('gamer', 'gamer@test.com', 'pass123')
        assert hasattr(user, 'perfil_gamer')
        assert user.perfil_gamer.level == 1
        assert user.perfil_gamer.dev_coins == 0
    
    def test_xp_to_next_level(self):
        user = User.objects.create_user('test', 'test@test.com', 'pass')
        perfil = user.perfil_gamer
        
        # Level 1: (1 * 100) * 1.5 = 150
        assert perfil.xp_to_next_level() == 150
        
        perfil.level = 5
        # Level 5: (5 * 100) * 1.5 = 750
        assert perfil.xp_to_next_level() == 750
    
    def test_adicionar_xp_level_up(self):
        user = User.objects.create_user('test', 'test@test.com', 'pass')
        perfil = user.perfil_gamer
        
        # Adiciona XP suficiente para subir de nível
        perfil.adicionar_xp(200)
        
        assert perfil.level == 2
        assert perfil.total_xp == 200
        assert perfil.current_xp == 50  # 200 - 150 (XP necessário para level 2)
    
    def test_adicionar_xp_multiplos_levels(self):
        user = User.objects.create_user('test', 'test@test.com', 'pass')
        perfil = user.perfil_gamer
        
        # Adiciona muito XP
        perfil.adicionar_xp(1000)
        
        assert perfil.level > 1
        assert perfil.total_xp == 1000

@pytest.mark.django_db
class TestSessaoGamer:
    def test_calcular_duracao(self):
        user = User.objects.create_user('test', 'test@test.com', 'pass')
        skill = SkillNode.objects.create(nome="Python")
        
        inicio = timezone.now()
        fim = inicio + timedelta(hours=2)
        
        sessao = SessaoGamer.objects.create(
            user=user,
            skill=skill,
            inicio=inicio,
            fim=fim,
            metodo='VIDEO'
        )
        
        assert sessao.duracao_minutos == 120
    
    def test_multiplicador_xp_video(self):
        user = User.objects.create_user('test', 'test@test.com', 'pass')
        skill = SkillNode.objects.create(nome="Python")
        
        inicio = timezone.now()
        fim = inicio + timedelta(hours=1)
        
        sessao = SessaoGamer.objects.create(
            user=user,
            skill=skill,
            inicio=inicio,
            fim=fim,
            metodo='VIDEO'
        )
        
        # 60 minutos * 1.0 = 60 XP
        assert sessao.xp_ganho == 60
        assert sessao.coins_ganhos == 30  # 60 * 0.5
    
    def test_multiplicador_xp_project(self):
        user = User.objects.create_user('test', 'test@test.com', 'pass')
        skill = SkillNode.objects.create(nome="Python")
        
        inicio = timezone.now()
        fim = inicio + timedelta(hours=1)
        
        sessao = SessaoGamer.objects.create(
            user=user,
            skill=skill,
            inicio=inicio,
            fim=fim,
            metodo='PROJECT'
        )
        
        # 60 minutos * 2.0 = 120 XP
        assert sessao.xp_ganho == 120
        assert sessao.coins_ganhos == 30
    
    def test_sessao_adiciona_xp_ao_perfil(self):
        user = User.objects.create_user('test', 'test@test.com', 'pass')
        skill = SkillNode.objects.create(nome="Python")
        perfil_inicial_xp = user.perfil_gamer.total_xp
        
        inicio = timezone.now()
        fim = inicio + timedelta(hours=1)
        
        SessaoGamer.objects.create(
            user=user,
            skill=skill,
            inicio=inicio,
            fim=fim,
            metodo='CODING'  # 1.5x
        )
        
        user.perfil_gamer.refresh_from_db()
        # 60 * 1.5 = 90 XP
        assert user.perfil_gamer.total_xp == perfil_inicial_xp + 90

@pytest.mark.django_db
class TestItemLoja:
    def test_criar_item(self):
        item = ItemLoja.objects.create(
            nome="Moldura Neon",
            categoria="FRAME",
            preco=500,
            raridade="RARO"
        )
        
        assert str(item) == "Moldura Neon (500 coins)"
    
    def test_inventario_usuario(self):
        user = User.objects.create_user('test', 'test@test.com', 'pass')
        item = ItemLoja.objects.create(nome="Item Teste", categoria="FRAME", preco=100)
        
        inventario = InventarioUsuario.objects.get(user=user)
        inventario.itens.add(item)
        
        assert item in inventario.itens.all()

@pytest.mark.django_db
class TestQuestEmprego:
    def test_criar_quest(self):
        recrutador = User.objects.create_user('recruiter', 'rec@test.com', 'pass')
        skill = SkillNode.objects.create(nome="Django")
        
        quest = QuestEmprego.objects.create(
            recrutador=recrutador,
            titulo="Dev Django Sênior",
            empresa="Tech Corp",
            descricao="Vaga para Django",
            salario="R$ 8.000",
            nivel_minimo=5,
            skill_requerida=skill
        )
        
        assert quest.ativa
        assert str(quest) == "Quest: Dev Django Sênior @ Tech Corp"

@pytest.mark.django_db
class TestBossBattle:
    def test_criar_boss(self):
        skill = SkillNode.objects.create(nome="Python")
        boss = BossBattle.objects.create(
            titulo="Clone do Twitter",
            descricao="Crie uma rede social",
            xp_recompensa=1000,
            coins_recompensa=500,
            dificuldade="MEDIO",
            skill_relacionada=skill
        )
        
        assert boss.ativo
        assert "MEDIO" in str(boss)
    
    def test_submissao_projeto(self):
        user = User.objects.create_user('test', 'test@test.com', 'pass')
        boss = BossBattle.objects.create(
            titulo="Boss Teste",
            descricao="Teste",
            xp_recompensa=500
        )
        
        submissao = SubmissaoProjeto.objects.create(
            user=user,
            boss=boss,
            repo_link="https://github.com/test/repo",
            descricao_solucao="Minha solução"
        )
        
        assert submissao.status == "PENDENTE"
        assert not submissao.sos_ativado

@pytest.mark.django_db
class TestCodeReview:
    def test_criar_review(self):
        user = User.objects.create_user('test', 'test@test.com', 'pass')
        ajudante = User.objects.create_user('helper', 'helper@test.com', 'pass')
        boss = BossBattle.objects.create(titulo="Boss", descricao="Test", xp_recompensa=100)
        
        submissao = SubmissaoProjeto.objects.create(
            user=user,
            boss=boss,
            repo_link="https://github.com/test/repo"
        )
        
        review = CodeReview.objects.create(
            submissao=submissao,
            autor=ajudante,
            role="BUG",
            conteudo="Encontrei um bug na linha 10"
        )
        
        assert not review.aceito
        assert review.xp_ajudante == 50
    
    def test_review_aceito_da_xp(self):
        user = User.objects.create_user('test', 'test@test.com', 'pass')
        ajudante = User.objects.create_user('helper', 'helper@test.com', 'pass')
        boss = BossBattle.objects.create(titulo="Boss", descricao="Test", xp_recompensa=100)
        
        submissao = SubmissaoProjeto.objects.create(
            user=user,
            boss=boss,
            repo_link="https://github.com/test/repo"
        )
        
        xp_inicial = ajudante.perfil_gamer.total_xp
        
        review = CodeReview.objects.create(
            submissao=submissao,
            autor=ajudante,
            role="BUG",
            conteudo="Bug corrigido",
            aceito=True
        )
        
        ajudante.perfil_gamer.refresh_from_db()
        assert ajudante.perfil_gamer.total_xp == xp_inicial + 50
