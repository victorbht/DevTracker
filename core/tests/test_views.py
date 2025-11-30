import pytest
from datetime import timedelta
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Tecnologia, MetodoEstudo, SessaoEstudo


@pytest.mark.django_db
class TestViews:
    
    @pytest.fixture
    def user(self):
        return User.objects.create_user('viewer', 'view@test.com', 'pass')
    
    @pytest.fixture
    def client_logged(self, client, user):
        client.force_login(user)
        return client
    
    @pytest.fixture
    def tech(self):
        return Tecnologia.objects.create(nome='Django')
    
    @pytest.fixture
    def metodo(self):
        return MetodoEstudo.objects.create(nome='Vídeo')
    
    def test_index_requer_login(self, client):
        response = client.get(reverse('core:index'))
        assert response.status_code == 302
    
    def test_index_logado(self, client_logged):
        response = client_logged.get(reverse('core:index'))
        assert response.status_code == 200
        assert 'perfil' in response.context
    
    def test_criar_sessao(self, client_logged, tech, metodo):
        from django.utils import timezone
        data = {
            'tecnologia': tech.id,
            'topico': 'Views',
            'metodo': metodo.id,
            'data_registro': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'tempo_liquido': '1:30:00',
            'qtd_exercicios': 10,
            'qtd_acertos': 8
        }
        response = client_logged.post(reverse('core:index'), data)
        assert SessaoEstudo.objects.count() == 1
        sessao = SessaoEstudo.objects.first()
        assert sessao.topico == 'Views'
        assert sessao.tempo_liquido == timedelta(hours=1, minutes=30)
    
    def test_editar_tempo_inline(self, client_logged, tech, metodo):
        sessao = SessaoEstudo.objects.create(
            tecnologia=tech,
            topico='Test',
            metodo=metodo,
            tempo_liquido=timedelta(hours=1)
        )
        response = client_logged.post(
            reverse('core:editar_tempo', args=[sessao.id]),
            {'tempo_liquido': '02:00:00'}
        )
        assert response.status_code == 200
        sessao.refresh_from_db()
        assert sessao.tempo_liquido == timedelta(hours=2)
    
    def test_excluir_sessao(self, client_logged, tech, metodo):
        sessao = SessaoEstudo.objects.create(
            tecnologia=tech,
            topico='Test',
            metodo=metodo,
            tempo_liquido=timedelta(hours=1)
        )
        response = client_logged.post(reverse('core:excluir', args=[sessao.id]))
        assert SessaoEstudo.objects.count() == 0
    
    def test_galeria_conquistas(self, client_logged):
        response = client_logged.get(reverse('core:conquistas'))
        assert response.status_code == 200
        assert 'todas_conquistas' in response.context
    
    def test_estatisticas(self, client_logged):
        response = client_logged.get(reverse('core:estatisticas'))
        assert response.status_code == 200
        assert 'evolucao_json' in response.context
    
    def test_salvar_tech(self, client_logged):
        response = client_logged.post(reverse('core:salvar_tech'), {'nome': 'React'})
        assert Tecnologia.objects.filter(nome='React').exists()
    
    def test_salvar_metodo(self, client_logged):
        response = client_logged.post(reverse('core:salvar_metodo'), {'nome': 'Livro'})
        assert MetodoEstudo.objects.filter(nome='Livro').exists()
    
    def test_salvar_metas(self, client_logged, user):
        response = client_logged.post(reverse('core:salvar_metas'), {
            'meta_semanal': 10,
            'meta_mensal': 40
        })
        user.perfil.refresh_from_db()
        assert user.perfil.meta_semanal == 10
        assert user.perfil.meta_mensal == 40
