# DevTracker — Dashboard Gamificado de Estudos

DevTracker é um painel Django para acompanhar horas líquidas de estudo de programação, com gamificação (XP, níveis, streaks e badges automáticas), CRUD via modais e gráficos em tempo real para tecnologias e métodos de estudo.

## Principais recursos
- Registro rápido de sessões com matéria, método, tempo líquido, exercícios e notas em Markdown.
- Engine de XP/Nível, streak diária e badges hexagonais inspiradas em Strava/Garmin.
- Dashboard dark/gamer com Bootstrap 5 + Chart.js e cards com progresso de nível.
- Galeria de conquistas com filtros visuais (streak, tecnologia e tempo total).
- CRUD completo (sessões, tecnologias e métodos) via modais e microinterações.

## Stack
- **Backend:** Django 5, SQLite (dev), ORM.
- **Frontend:** Bootstrap 5 (dark/gamer), Chart.js, Font Awesome.
- **Extras:** widget-tweaks (forms), markdown (render de notas).
- **Testes:** pytest, pytest-django, pytest-cov (81% coverage).

## Como rodar localmente

### Opção 1: Docker (Recomendado)
Pré-requisitos: Docker e Docker Compose.

```bash
git clone https://github.com/<seu-usuario>/DevTracker.git
cd DevTracker

# Copiar variáveis de ambiente
cp .env.example .env

# Subir containers
docker-compose up -d

# Criar superusuário
docker-compose exec web python manage.py createsuperuser
```

Acesse: `http://localhost:8000`

### Opção 2: Local (SQLite)
Pré-requisitos: Python 3.12+ e Pipenv.

```bash
git clone https://github.com/<seu-usuario>/DevTracker.git
cd DevTracker
pipenv install
pipenv shell

# Variáveis de ambiente (exemplo para desenvolvimento)
export DJANGO_SECRET_KEY="dev-secret-key"
export DJANGO_DEBUG=True

python manage.py migrate
python manage.py seed_badges
python manage.py createsuperuser
python manage.py runserver
```

Acesse: `http://localhost:8000`

## Testes

```bash
# Instalar dependências de teste
pipenv install --dev

# Rodar todos os testes
pipenv run pytest

# Com coverage
pipenv run pytest --cov=core --cov-report=term-missing

# Testes específicos
pipenv run pytest core/tests/test_gamification.py -v
```

**Coverage atual: 81%** ✅

## Melhorias Implementadas

Veja [CHANGELOG.md](CHANGELOG.md) para lista completa de melhorias.

### Destaques:
- ✅ Botão "Repetir Última Sessão"
- ✅ Edição rápida de tempo (double-click)
- ✅ Página dedicada de estatísticas
- ✅ Gráfico de evolução temporal
- ✅ Sistema de metas (semanal/mensal)
- ✅ Atalhos de teclado (Ctrl+N, Ctrl+K)
- ✅ Exportação CSV/JSON
- ✅ Validações e confirmações
- ✅ Testes automatizados (pytest)

## Deploy

Veja [DEPLOY.md](DEPLOY.md) para guia completo de deploy em produção.

## Dados e gamificação
- **Modelos centrais:** `SessaoEstudo` (tempo líquido, método, tecnologia, anotações), `Tecnologia`, `MetodoEstudo`, `Conquista`, `PerfilUsuario`.
- **XP/Nível:** XP acumulado pelas conquistas; nível sobe a cada 1000 XP.
- **Streak (Ofensiva):** contador diário contínuo calculado a partir de sessões.
- **Badges automáticas:** horas por tecnologia, horas totais e streaks. Popule com `python manage.py seed_badges` (ou `/setup-badges/` restrito a staff).

## Estrutura rápida
```
core/
  badges.py                # definição e seed das conquistas
  management/commands/     # comando seed_badges
  models.py | views.py     # regras de XP, streak e dashboard
  templates/core/          # index e galeria de conquistas
  tests/                   # testes automatizados
    test_models.py         # testes de modelos
    test_gamification.py   # testes de XP/streak/conquistas
    test_views.py          # testes de views/CRUD
devtracker/settings.py     # configs usando variáveis de ambiente
pytest.ini                 # configuração pytest
.github/workflows/         # CI/CD com GitHub Actions
```

## Pontos de UI/UX para mostrar no portfólio
- Paleta neon (verde/azul) com elementos glassmorphism e cards de progresso.
- Modais de CRUD para fluxo rápido e sem reload.
- Badges hexagonais com clip-path e ícones Font Awesome.
- Gráficos dinâmicos (pizza/barra) para distribuição por tecnologia e método.
- Galeria de conquistas com estados locked/unlocked e ribbon de destaque.

## Próximos Passos

### Prioridade Alta
- [x] Testes automatizados (pytest) ✅
- [x] Docker + PostgreSQL ✅
- [ ] Deploy (Railway/Fly/Render)
- [x] CI/CD com GitHub Actions ✅

### Prioridade Média
- [ ] Templates de sessão
- [ ] Busca full-text em anotações
- [ ] Histórico de níveis
- [ ] Pomodoro timer integrado

### Prioridade Baixa
- [ ] Perfil público compartilhável
- [ ] API REST
- [ ] Integração GitHub
- [ ] App mobile

## Licença

MIT License - Sinta-se livre para usar em seus projetos!
