import pytest
from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Tecnologia, MetodoEstudo, SessaoEstudo, Conquista, PerfilUsuario


@pytest.mark.django_db
class TestModels:
    
    def test_perfil_criado_automaticamente(self):
        user = User.objects.create_user('test', 'test@test.com', 'pass')
        assert hasattr(user, 'perfil')
        assert user.perfil.xp_total == 0
        assert user.perfil.nivel == 1
    
    def test_tecnologia_str(self):
        tech = Tecnologia.objects.create(nome='Python')
        assert str(tech) == 'Python'
    
    def test_metodo_str(self):
        metodo = MetodoEstudo.objects.create(nome='Vídeo')
        assert str(metodo) == 'Vídeo'
    
    def test_sessao_criacao(self):
        tech = Tecnologia.objects.create(nome='Django')
        metodo = MetodoEstudo.objects.create(nome='Prática')
        sessao = SessaoEstudo.objects.create(
            tecnologia=tech,
            topico='Models',
            metodo=metodo,
            tempo_liquido=timedelta(hours=2)
        )
        assert sessao.tecnologia.nome == 'Django'
        assert sessao.tempo_liquido.total_seconds() == 7200
    
    def test_conquista_criacao(self):
        conquista = Conquista.objects.create(
            nome='Primeira Hora',
            descricao='Complete 1 hora',
            categoria='tempo',
            quantidade_necessaria=1,
            xp_reward=100
        )
        assert conquista.xp_reward == 100
        assert conquista.categoria == 'tempo'
