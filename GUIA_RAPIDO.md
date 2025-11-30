# 🚀 Guia R\u00e1pido - DevTracker RPG

## Primeiros Passos

### 1. Configurar Ambiente

```bash
# Clonar reposit\u00f3rio
git clone https://github.com/<seu-usuario>/DevTracker.git
cd DevTracker

# Instalar depend\u00eancias
pipenv install
pipenv shell

# Configurar vari\u00e1veis de ambiente
export DJANGO_SECRET_KEY="dev-secret-key"
export DJANGO_DEBUG=True

# Migrar banco de dados
python manage.py migrate

# Popular badges e conte\u00fado inicial
python manage.py seed_badges_rpg
python manage.py seed_gamer_pack

# Criar superusu\u00e1rio
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver
```

### 2. Acessar Dashboard
Abra o navegador em: `http://localhost:8000/gamer/`

---

## Funcionalidades Principais

### 📊 Dashboard RPG
**Rota**: `/gamer/`

**O que voc\u00ea v\u00ea**:
- Hero Card: Avatar, n\u00edvel, XP, progress bar
- Streak Card: Dias consecutivos + fire animation
- DevCoins Card: Moeda virtual (link para loja)
- Daily Quest: Check-in di\u00e1rio (15min = +10 coins)
- Skill Tree Preview: Top 3 skills desenvolvidas
- Boss Ativo: Pr\u00f3ximo desafio dispon\u00edvel
- Log de Miss\u00f5es: \u00daltimas 5 sess\u00f5es
- Conquistas Recentes: \u00daltimas 3 badges desbloqueadas

**A\u00e7\u00f5es**:
- Clicar em "INICIAR NOVA SESS\u00c3O" → Abre modal
- Clicar em DevCoins → Vai para loja
- Clicar em "ACEITAR DESAFIO" → Vai para arena do boss

---

### ⚔️ Boss Battles
**Rota**: `/gamer/quests/` (lista) | `/gamer/arena/<boss_id>/` (detalhes)

**Como funciona**:
1. Acesse a lista de quests
2. Escolha um boss (verifique requisitos de skill/level)
3. Clique em "Ver Detalhes"
4. Leia a descri\u00e7\u00e3o do desafio
5. Submeta link do reposit\u00f3rio GitHub
6. Marque "SOS" se precisar de ajuda (code review)
7. Aguarde valida\u00e7\u00e3o (admin aprova)
8. Receba recompensas (XP + DevCoins)

**Recompensas por Tier**:
- **Comum**: 500 XP + 100 Coins
- **Raro**: 1000 XP + 300 Coins
- **\u00c9pico**: 2000 XP + 800 Coins
- **Lend\u00e1rio**: 3000 XP + 1500 Coins

---

### 🛒 Loja de Cosm\u00e9ticos
**Rota**: `/gamer/inventario/`

**Itens dispon\u00edveis**:
- Molduras de avatar
- Banners de perfil
- Temas de dashboard
- Badges especiais

**Como comprar**:
1. Acumule DevCoins estudando
2. Acesse a loja
3. Clique em "Comprar" no item desejado
4. Item vai para seu invent\u00e1rio
5. Equipe no perfil

---

### 🌳 Skill Tree
**Rota**: `/gamer/skills/` (em desenvolvimento)

**Como funciona**:
- Cada tecnologia \u00e9 uma skill (Python, Django, React, etc.)
- Skills ganham XP quando voc\u00ea estuda
- A cada 100 XP, skill sobe 1 n\u00edvel
- Skills desbloqueiam outras (ex: Python → Django)
- N\u00edvel da skill afeta multiplicador de XP

**Multiplicadores de M\u00e9todo**:
- V\u00eddeo: 1.0x
- Leitura: 1.2x
- C\u00f3digo: 1.5x
- Projeto: 2.0x

---

## Sistema de Gamifica\u00e7\u00e3o

### XP e N\u00edveis
- **F\u00f3rmula**: `XP = Tempo (min) × Multiplicador do M\u00e9todo`
- **Level-up**: A cada 1000 XP acumulados
- **Benef\u00edcios**: Desbloqueia bosses mais dif\u00edceis

### Streak (Ofensiva)
- **Como funciona**: Estude pelo menos 1x por dia
- **Prote\u00e7\u00e3o**: Streak Freeze (compre na loja ou ganhe em badges)
- **Recompensas**: Badges especiais aos 7, 30, 100 dias

### Badges (Conquistas)
**16 badges divididas em 4 categorias**:

#### 1. Grind (Tempo Total)
- Hello World: 1h
- Maratonista: 50h
- Centuri\u00e3o: 100h
- Mestre: 500h

#### 2. Behavior (H\u00e1bitos)
- Night Owl: 20h ap\u00f3s 22h
- Early Bird: 20h antes das 8h
- On Fire: 7 dias de streak
- Consistency King: 30 dias de streak

#### 3. Skills (Tecnologias)
- Snake Charmer: 20h de Python
- Code Master: 50h de qualquer skill

#### 4. Social (Colabora\u00e7\u00e3o)
- Senpai: Ajudar 5 code reviews
- Mentor: Ajudar 20 code reviews

---

## Comandos \u00dateis

### Gerenciar Banco de Dados
```bash
# Criar nova migra\u00e7\u00e3o
python manage.py makemigrations

# Aplicar migra\u00e7\u00f5es
python manage.py migrate

# Resetar banco (CUIDADO: apaga tudo)
rm db.sqlite3
python manage.py migrate
```

### Popular Dados Iniciais
```bash
# Badges RPG (16 conquistas)
python manage.py seed_badges_rpg

# Pacote Gamer (skills, bosses, itens)
python manage.py seed_gamer_pack

# Ambos
python manage.py seed_badges_rpg && python manage.py seed_gamer_pack
```

### Testes
```bash
# Rodar todos os testes
pytest

# Com coverage
pytest --cov=core --cov-report=term-missing

# Testes espec\u00edficos
pytest core/tests/test_gamer_pack.py -v
```

### Admin Django
```bash
# Acessar painel admin
http://localhost:8000/admin/

# Login com superusu\u00e1rio criado anteriormente
```

---

## Atalhos de Teclado

- `Ctrl + N`: Nova sess\u00e3o (abre modal)
- `Ctrl + K`: Busca r\u00e1pida
- `Esc`: Fechar modal

---

## Dicas de Uso

### Maximizar XP
1. **Use m\u00e9todo "Projeto"**: 2.0x multiplicador
2. **Mantenha streak ativo**: Badges de streak d\u00e3o muito XP
3. **Complete bosses**: Recompensas \u00e9picas
4. **Daily quest**: 15min di\u00e1rios = +10 coins

### Ganhar DevCoins R\u00e1pido
1. **Estude 1h por dia**: ~12 coins/dia
2. **Daily quest**: +10 coins/dia
3. **Desbloqueie badges**: +50-200 coins cada
4. **Complete bosses**: +100-1500 coins

### Desbloquear Badges
1. **Grind**: Apenas estude (tempo acumula)
2. **Behavior**: Estude em hor\u00e1rios espec\u00edficos
3. **Skills**: Foque em uma tecnologia
4. **Social**: Ajude outros devs (code review)

---

## Troubleshooting

### Erro: "No module named 'core'"
```bash
# Certifique-se de estar no diret\u00f3rio correto
cd DevTracker
pipenv shell
```

### Erro: "Table doesn't exist"
```bash
# Rode as migra\u00e7\u00f5es
python manage.py migrate
```

### Badges n\u00e3o aparecem
```bash
# Popular badges
python manage.py seed_badges_rpg
```

### XP n\u00e3o est\u00e1 sendo calculado
- Verifique se o signal est\u00e1 ativo em `core/signals.py`
- Certifique-se de que `apps.py` tem `ready()` configurado

### Streak n\u00e3o atualiza
- Verifique timezone em `settings.py`
- Confirme que `last_checkin` est\u00e1 sendo salvo

---

## Estrutura de Pastas

```
DevTracker/
\u251c\u2500\u2500 core/                      # App principal
\u2502   \u251c\u2500\u2500 models.py              # Modelos (UserProfile, StudySession, etc.)
\u2502   \u251c\u2500\u2500 views.py               # Views (dashboard, quests, arena)
\u2502   \u251c\u2500\u2500 signals.py             # Auto XP/badges
\u2502   \u251c\u2500\u2500 achievements.py        # L\u00f3gica de badges
\u2502   \u251c\u2500\u2500 admin.py               # Painel admin
\u2502   \u251c\u2500\u2500 urls.py                # Rotas
\u2502   \u251c\u2500\u2500 templates/core/        # Templates HTML
\u2502   \u2502   \u251c\u2500\u2500 dashboard_rpg.html
\u2502   \u2502   \u251c\u2500\u2500 quests.html
\u2502   \u2502   \u251c\u2500\u2500 arena.html
\u2502   \u2502   \u2514\u2500\u2500 inventory.html
\u2502   \u251c\u2500\u2500 management/commands/  # Comandos customizados
\u2502   \u2502   \u251c\u2500\u2500 seed_badges_rpg.py
\u2502   \u2502   \u2514\u2500\u2500 seed_gamer_pack.py
\u2502   \u2514\u2500\u2500 tests/                # Testes automatizados
\u251c\u2500\u2500 devtracker/               # Configura\u00e7\u00f5es Django
\u2502   \u251c\u2500\u2500 settings.py
\u2502   \u251c\u2500\u2500 urls.py
\u2502   \u2514\u2500\u2500 wsgi.py
\u251c\u2500\u2500 static/                   # Arquivos est\u00e1ticos
\u251c\u2500\u2500 db.sqlite3                # Banco de dados (dev)
\u251c\u2500\u2500 manage.py
\u251c\u2500\u2500 Pipfile                   # Depend\u00eancias
\u251c\u2500\u2500 pytest.ini                # Config testes
\u251c\u2500\u2500 README.md
\u251c\u2500\u2500 GAME_DESIGN_DOCUMENT.md
\u251c\u2500\u2500 MELHORIAS_DASHBOARD.md
\u2514\u2500\u2500 GUIA_RAPIDO.md
```

---

## Recursos Adicionais

- **Documenta\u00e7\u00e3o Django**: https://docs.djangoproject.com/
- **Bootstrap 5**: https://getbootstrap.com/docs/5.0/
- **Font Awesome**: https://fontawesome.com/icons
- **Chart.js**: https://www.chartjs.org/

---

## Suporte

- **Issues**: https://github.com/<seu-usuario>/DevTracker/issues
- **Discuss\u00f5es**: https://github.com/<seu-usuario>/DevTracker/discussions

---

## Licen\u00e7a

MIT License - Projeto open-source para portf\u00f3lio
