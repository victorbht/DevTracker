# 🎮 PACOTE GAMER - DevTracker RPG Edition

## Visão Geral

O **Pacote Gamer** transforma o DevTracker em uma experiência RPG completa, adicionando elementos de jogos modernos como árvore de habilidades, loja de cosméticos, boss battles e sistema de party/cooperação.

## 🆕 Novos Recursos

### 1. 🌳 Árvore de Habilidades (Skill Tree)
- Sistema hierárquico de tecnologias (ex: Python → Django, Flask)
- Desbloqueio progressivo baseado em estudo
- Visualização em árvore interativa
- Ícones personalizados para cada skill

**Modelo:** `SkillNode`

### 2. 👤 Perfil Gamer Avançado
- **Level System:** Progressão RPG com fórmula exponencial
- **DevCoins:** Moeda virtual ganha estudando
- **Cosméticos:** Molduras de avatar e banners equipáveis
- **Bio Pública:** Perfil compartilhável com link GitHub
- **Skills Desbloqueadas:** Registro de tecnologias dominadas

**Modelo:** `PerfilGamer`

### 3. ⚡ Sessões com Multiplicadores
Sistema de XP dinâmico baseado no método de estudo:

| Método | Multiplicador | XP por hora |
|--------|---------------|-------------|
| 📺 Vídeo Aula | 1.0x | 60 XP |
| 📖 Leitura/Docs | 1.2x | 72 XP |
| 💻 Codificação | 1.5x | 90 XP |
| 🚀 Projeto Prático | 2.0x | 120 XP |

**Modelo:** `SessaoGamer`

### 4. 🛒 Loja de Cosméticos
- **Molduras de Avatar:** Comum, Raro, Épico, Lendário
- **Banners de Perfil:** Temas cyberpunk, matrix, neon
- **Temas UI:** Personalize a interface
- Compra com DevCoins ganhos estudando

**Modelos:** `ItemLoja`, `InventarioUsuario`

### 5. 💼 Quests de Emprego
- Vagas reais gamificadas como missões
- Requisitos de nível e skills
- Recrutadores podem postar vagas
- Sistema de match baseado em perfil

**Modelo:** `QuestEmprego`

### 6. ⚔️ Boss Battles (Desafios PBL)
Projetos práticos como chefes de RPG:

- **⭐ Fácil:** Clone do Twitter (1000 XP)
- **⭐⭐ Médio:** API REST Completa (800 XP)
- **⭐⭐⭐ Difícil:** Dashboard Analytics (1500 XP)
- **⭐⭐⭐⭐ Lendário:** E-commerce Full Stack (3000 XP)

**Modelo:** `BossBattle`

### 7. 🤝 Sistema de Party (Code Review)
Cooperação entre usuários com papéis RPG:

- **🐛 Clérigo:** Especialista em Bug Fix
- **⚡ Ferreiro:** Otimização de performance
- **🎨 Bardo:** Melhorias de estilo/UX
- **🏗️ Arquiteto:** Refatoração de estrutura

**Modelos:** `SubmissaoProjeto`, `CodeReview`

## 📦 Instalação

### 1. Aplicar Migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Popular Dados Iniciais

```bash
python manage.py seed_gamer_pack
```

Isso criará:
- ✅ 10 skills na árvore (Python, Django, React, etc.)
- ✅ 6 itens cosméticos na loja
- ✅ 4 boss battles de diferentes dificuldades

### 3. Criar Perfis Gamer

Os perfis são criados automaticamente quando um usuário é registrado. Para usuários existentes:

```python
from django.contrib.auth.models import User
from core.models import PerfilGamer, InventarioUsuario

for user in User.objects.all():
    PerfilGamer.objects.get_or_create(user=user)
    InventarioUsuario.objects.get_or_create(user=user)
```

## 🎯 Casos de Uso

### Estudante Iniciante
1. Cria conta → Ganha perfil Level 1
2. Estuda Python por 2h (vídeo) → Ganha 120 XP + 60 DevCoins
3. Compra "Moldura Neon Verde" (500 coins)
4. Tenta Boss Battle "API REST" → Pede SOS
5. Recebe ajuda de um "Clérigo" → Aprova o projeto
6. Ganha 800 XP → Sobe para Level 3

### Desenvolvedor Avançado
1. Level 10+ → Desbloqueia Quests de Emprego
2. Completa Boss "E-commerce" → Ganha 3000 XP
3. Ajuda 5 iniciantes → Ganha 250 XP de bônus
4. Compra "Moldura Lendária" (2000 coins)
5. Perfil público mostra conquistas → Recrutador vê

### Recrutador
1. Posta Quest "Vaga Sênior Django"
2. Define: Level mínimo 8, Skill Django
3. Sistema filtra candidatos automaticamente
4. Candidatos aplicam com portfólio de Boss Battles

## 🎨 Integração com UI

### Cards de Perfil
```html
<div class="profile-card {{ user.perfil_gamer.equipped_frame.css_class }}">
  <img src="{{ user.avatar }}" alt="Avatar">
  <div class="level-badge">Lvl {{ user.perfil_gamer.level }}</div>
  <div class="xp-bar">
    <div class="xp-fill" style="width: {{ xp_percentage }}%"></div>
  </div>
</div>
```

### Skill Tree Visualization
```javascript
// Usar D3.js ou vis.js para árvore interativa
const skillTree = {
  name: "Python",
  children: [
    { name: "Django", unlocked: true },
    { name: "Flask", unlocked: false }
  ]
};
```

### Boss Battle Card
```html
<div class="boss-card difficulty-{{ boss.dificuldade }}">
  <i class="{{ boss.boss_icon }} boss-icon"></i>
  <h3>{{ boss.titulo }}</h3>
  <div class="rewards">
    <span>🏆 {{ boss.xp_recompensa }} XP</span>
    <span>💰 {{ boss.coins_recompensa }} Coins</span>
  </div>
  <button class="btn-challenge">Desafiar Boss</button>
</div>
```

## 📊 Estatísticas e Analytics

### Métricas do Pacote Gamer
- Total de XP ganho por método
- Skills mais estudadas
- Boss Battles completados
- Code Reviews dados/recebidos
- DevCoins gastos vs ganhos
- Taxa de conclusão de projetos

### Leaderboards
- Top 10 por Level
- Top 10 por Boss Battles
- Top 10 Ajudantes (Code Reviews)
- Top 10 por Skill específica

## 🔧 Configurações Avançadas

### Ajustar Multiplicadores de XP
```python
# core/models.py - SessaoGamer.MULTIPLICADORES
MULTIPLICADORES = {
    'VIDEO': 1.0,
    'READING': 1.5,  # Aumentar leitura
    'CODING': 2.0,   # Aumentar prática
    'PROJECT': 3.0,  # Aumentar projetos
}
```

### Fórmula de Level Up
```python
# core/models.py - PerfilGamer.xp_to_next_level()
def xp_to_next_level(self):
    # Padrão: (level * 100) * 1.5
    # Mais fácil: level * 100
    # Mais difícil: (level ** 2) * 50
    return int((self.level * 100) * 1.5)
```

### Preços da Loja
```python
# Ajustar em core/management/commands/seed_gamer_pack.py
itens_data = [
    {'nome': 'Item Comum', 'preco': 100},
    {'nome': 'Item Raro', 'preco': 500},
    {'nome': 'Item Épico', 'preco': 1000},
    {'nome': 'Item Lendário', 'preco': 5000},
]
```

## 🚀 Próximos Passos

### Prioridade Alta
- [ ] Views e templates para Skill Tree
- [ ] Página da Loja com sistema de compra
- [ ] Interface de Boss Battles
- [ ] Sistema de Code Review (chat/comentários)

### Prioridade Média
- [ ] Leaderboards globais
- [ ] Perfil público compartilhável
- [ ] Notificações de level up
- [ ] Animações de conquistas

### Prioridade Baixa
- [ ] Sistema de guilds/equipes
- [ ] Torneios de Boss Battles
- [ ] Marketplace de itens entre usuários
- [ ] Integração com Discord

## 🎮 Gamification Best Practices

1. **Feedback Imediato:** Mostrar XP/Coins ganhos após cada sessão
2. **Progressão Visível:** Barra de XP sempre visível
3. **Recompensas Variadas:** Mix de XP, coins e itens
4. **Desafios Balanceados:** Boss Battles de todas dificuldades
5. **Social:** Code Reviews incentivam comunidade
6. **Personalização:** Cosméticos dão identidade

## 📝 Licença

Parte do projeto DevTracker - MIT License

---

**Desenvolvido com 💚 para gamificar o aprendizado de programação!**
