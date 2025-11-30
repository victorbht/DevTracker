import pytest
from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Tecnologia, MetodoEstudo, SessaoEstudo, Conquista, PerfilUsuario
from core.views import verificar_conquistas


@pytest.mark.django_db
class TestGamification:
    
    @pytest.fixture
    def user(self):
        return User.objects.create_user('gamer', 'gamer@test.com', 'pass')
    
    @pytest.fixture
    def tech(self):
        return Tecnologia.objects.create(nome='Python')
    
    @pytest.fixture
    def metodo(self):
        return MetodoEstudo.objects.create(nome='Prática')
    
    def test_xp_inicial(self, user):
        assert user.perfil.xp_total == 0
        assert user.perfil.nivel == 1
    
    def test_conquista_tempo_total(self, user, tech, metodo):
        Conquista.objects.create(
            nome='1 Hora',
            descricao='Complete 1 hora',
            categoria='tempo',
            quantidade_necessaria=1,
            xp_reward=100
        )
        SessaoEstudo.objects.create(
            tecnologia=tech,
            topico='Test',
            metodo=metodo,
            tempo_liquido=timedelta(hours=1)
        )
        novas, _ = verificar_conquistas(user)
        user.perfil.refresh_from_db()
        assert len(novas) == 1
        assert user.perfil.xp_total == 100
    
    def test_level_up(self, user, tech, metodo):
        for i in range(10):
            Conquista.objects.create(
                nome=f'Badge {i}',
                descricao='Test',
                categoria='tempo',
                quantidade_necessaria=i,
                xp_reward=100
            )
        SessaoEstudo.objects.create(
            tecnologia=tech,
            topico='Test',
            metodo=metodo,
            tempo_liquido=timedelta(hours=10)
        )
        verificar_conquistas(user)
        user.perfil.refresh_from_db()
        assert user.perfil.xp_total >= 1000
        assert user.perfil.nivel >= 2
    
    def test_streak_1_dia(self, user, tech, metodo):
        Conquista.objects.create(
            nome='Streak 1',
            descricao='1 dia',
            categoria='streak',
            quantidade_necessaria=1,
            xp_reward=50
        )
        SessaoEstudo.objects.create(
            tecnologia=tech,
            topico='Test',
            metodo=metodo,
            tempo_liquido=timedelta(hours=1),
            data_registro=timezone.now()
        )
        novas, streak = verificar_conquistas(user)
        assert streak >= 1
        assert len(novas) == 1
    
    def test_conquista_tecnologia_especifica(self, user, tech, metodo):
        Conquista.objects.create(
            nome='Python 5h',
            descricao='5 horas Python',
            categoria='tecnologia',
            tecnologia_alvo=tech,
            quantidade_necessaria=5,
            xp_reward=200
        )
        SessaoEstudo.objects.create(
            tecnologia=tech,
            topico='Test',
            metodo=metodo,
            tempo_liquido=timedelta(hours=5)
        )
        novas, _ = verificar_conquistas(user)
        user.perfil.refresh_from_db()
        assert len(novas) == 1
        assert user.perfil.xp_total == 200
    
    def test_conquista_metodo_especifico(self, user, tech, metodo):
        Conquista.objects.create(
            nome='Prática 3h',
            descricao='3 horas prática',
            categoria='metodo',
            metodo_alvo=metodo,
            quantidade_necessaria=3,
            xp_reward=150
        )
        SessaoEstudo.objects.create(
            tecnologia=tech,
            topico='Test',
            metodo=metodo,
            tempo_liquido=timedelta(hours=3)
        )
        novas, _ = verificar_conquistas(user)
        user.perfil.refresh_from_db()
        assert len(novas) == 1
        assert user.perfil.xp_total == 150
    
    def test_nao_desbloqueia_duas_vezes(self, user, tech, metodo):
        Conquista.objects.create(
            nome='1 Hora',
            descricao='Complete 1 hora',
            categoria='tempo',
            quantidade_necessaria=1,
            xp_reward=100
        )
        SessaoEstudo.objects.create(
            tecnologia=tech,
            topico='Test',
            metodo=metodo,
            tempo_liquido=timedelta(hours=2)
        )
        novas1, _ = verificar_conquistas(user)
        novas2, _ = verificar_conquistas(user)
        user.perfil.refresh_from_db()
        assert len(novas1) == 1
        assert len(novas2) == 0
        assert user.perfil.xp_total == 100
