# 🎮 Game Design Document - DevTracker RPG

## 1. Visão Geral

DevTracker não é apenas um "CRUD com CSS bonito" - é um **produto viciante** que transforma o aprendizado em uma experiência de jogo completa.

## 2. Economia e Progressão

### 2.1 Fórmula de XP (Curva Exponencial)

```python
XP_Necessario = Base × (Nivel)^1.5
Base = 100 XP (~1h de estudo em vídeo)
```

### 2.2 Tabela de Progressão

| Nível | Título (Rank) | XP p/ Próximo | Tempo Estimado |
|-------|---------------|---------------|----------------|
| 1-5 | Noob / Estagiário | 100 → 350 XP | 1h a 5h (Rápido!) |
| 6-15 | Júnior Dev | 400 → 1.800 XP | ~2 semanas |
| 16-30 | Pleno Dev | 2.000 → 5.000 XP | ~2 a 3 meses |
| 31-50 | Sênior Dev | 5.500 → 15.000 XP | ~6 meses |
| 50+ | Tech Lead / Architect | 15.000+ XP | Longo prazo |

### 2.3 Multiplicadores de XP

| Método | Multiplicador | XP/Hora | Uso Recomendado |
|--------|---------------|---------|-----------------|
| 📺 VIDEO | 1.0x | 60 XP | Aprendizado passivo |
| 📖 READING | 1.2x | 72 XP | Documentação |
| 💻 CODING | 1.5x | 90 XP | Prática ativa |
| 🚀 PROJECT | 2.0x | 120 XP | Projetos reais |

## 3. Sistema de Moedas (DevCoins)

### 3.1 Como Ganhar DevCoins

- **Estudando:** 1 coin a cada 5 minutos (12 coins/hora)
- **Check-in Diário:** 10-50 coins (escalonado)
- **Completando Quests:** 50-200 coins
- **Code Reviews Aceitos:** 25 coins por review
- **Boss Battles:** 100-500 coins

### 3.2 Economia Balanceada

**Regra de Ouro:** O item mais legal deve custar **30-50 horas de estudo**

| Item | Preço | Horas Necessárias |
|------|-------|-------------------|
| Moldura Básica | 500 coins | ~42h |
| Streak Freeze | 500 coins | ~42h |
| Moldura Rara | 1.000 coins | ~83h |
| Banner Épico | 2.000 coins | ~167h |
| Moldura Lendária | 5.000 coins | ~417h |

### 3.3 Premium (R$ 14,90/mês)

**Benefícios:**
- 2x DevCoins por hora
- Acesso à Loja Premium
- Analytics Avançados
- Vagas em Destaque
- 3 Streak Freezes grátis/mês

## 4. Sistema de Badges (Conquistas)

### 4.1 Badges de Grind (Persistência)

| Badge | Condição | XP Bônus | Coins Bônus |
|-------|----------|----------|-------------|
| Hello World | Primeira sessão | 50 XP | 10 coins |
| Maratonista | 4h seguidas | 200 XP | 50 coins |
| Centurião | 100h totais | 500 XP | 100 coins |
| 10.000 Horas | 10.000h totais | 5.000 XP | 1.000 coins |

### 4.2 Badges de Habilidade (Skill Tree)

| Badge | Condição | XP Bônus | Coins Bônus |
|-------|----------|----------|-------------|
| Snake Charmer | 50h em Python | 300 XP | 75 coins |
| Fullstack Hero | 50h Back + 50h Front | 500 XP | 150 coins |
| Bug Hunter | 10 Boss Battles | 400 XP | 100 coins |
| Code Master | 500h de CODING | 1.000 XP | 250 coins |

### 4.3 Badges de Comportamento (Hábitos)

| Badge | Condição | XP Bônus | Coins Bônus |
|-------|----------|----------|-------------|
| Night Owl | Sessão 02:00-05:00 | 100 XP | 25 coins |
| Early Bird | Sessão antes 06:00 | 100 XP | 25 coins |
| Weekend Warrior | 4 fins de semana seguidos | 300 XP | 75 coins |
| Consistency King | 30 dias de streak | 500 XP | 150 coins |

### 4.4 Badges Sociais (Comunidade)

| Badge | Condição | XP Bônus | Coins Bônus |
|-------|----------|----------|-------------|
| Senpai | 5 Code Reviews aceitos | 200 XP | 50 coins |
| Mentor | 20 Code Reviews aceitos | 500 XP | 150 coins |
| Líder de Guilda | Criar grupo 5+ pessoas | 300 XP | 100 coins |

## 5. Sistema de Streak (Retenção)

### 5.1 Mecânica de Check-in Diário

**Condição:** Registrar pelo menos 15 minutos de estudo

| Dia | Recompensa |
|-----|------------|
| Dia 1 | 10 coins + 50 XP |
| Dia 2 | 20 coins + 10% XP Boost (24h) |
| Dia 3 | 30 coins |
| Dia 4 | 40 coins |
| Dia 5 | 50 coins + Badge "On Fire" |
| Dia 6 | 60 coins |
| Dia 7 | 100 coins + Item Raro + Streak Freeze |

### 5.2 Streak Freeze (Congelador)

**Função:** Permite falhar 1 dia sem perder o streak  
**Custo:** 500 DevCoins  
**Limite:** 3 ativos simultaneamente  
**Premium:** 3 grátis por mês

## 6. Boss Battles (Desafios PBL)

### 6.1 Níveis de Dificuldade

| Dificuldade | XP Reward | Coins Reward | Tempo Estimado |
|-------------|-----------|--------------|----------------|
| ⭐ Fácil | 500 XP | 100 coins | 2-4h |
| ⭐⭐ Médio | 1.000 XP | 200 coins | 8-12h |
| ⭐⭐⭐ Difícil | 2.000 XP | 400 coins | 20-30h |
| ⭐⭐⭐⭐ Lendário | 5.000 XP | 1.000 coins | 50-100h |

### 6.2 Exemplos de Boss Battles

**Fácil:**
- Calculadora Python
- To-Do List
- Conversor de Moedas

**Médio:**
- API REST com Django
- Blog com autenticação
- Dashboard com gráficos

**Difícil:**
- E-commerce completo
- Rede social
- Sistema de chat real-time

**Lendário:**
- Clone do Netflix
- Plataforma de cursos
- Sistema bancário

## 7. Sistema de Party (Code Review)

### 7.1 Papéis RPG

| Papel | Função | XP por Review |
|-------|--------|---------------|
| 🐛 Clérigo | Bug Fix | 50 XP |
| ⚡ Ferreiro | Otimização | 75 XP |
| 🎨 Bardo | Estilo/UX | 50 XP |
| 🏗️ Arquiteto | Refatoração | 100 XP |

### 7.2 Mecânica SOS

- Usuário marca "SOS Ativado" na submissão
- Comunidade vê no feed de ajuda
- Quem ajudar ganha XP + coins
- Submissor pode aceitar/rejeitar review

## 8. Métricas de Sucesso (KPIs)

### 8.1 Retenção

- **D1 (Day 1):** 70% dos usuários voltam no dia seguinte
- **D7 (Day 7):** 40% dos usuários voltam após 7 dias
- **D30 (Day 30):** 20% dos usuários voltam após 30 dias

### 8.2 Engajamento

- **Sessões/Semana:** Média de 4 sessões por usuário
- **Tempo Médio:** 45 minutos por sessão
- **Streak Médio:** 5 dias consecutivos

### 8.3 Monetização

- **Conversão Premium:** 5% dos usuários ativos
- **LTV (Lifetime Value):** R$ 150 por usuário premium
- **Churn Rate:** <10% ao mês

## 9. Roadmap de Features

### Fase 1 (MVP) ✅
- [x] Sistema de XP e Levels
- [x] Multiplicadores de método
- [x] DevCoins básico
- [x] Boss Battles
- [x] Code Reviews

### Fase 2 (Retenção)
- [ ] Sistema de Badges completo
- [ ] Streak com check-in diário
- [ ] Streak Freeze
- [ ] Loja de cosméticos
- [ ] Dashboard RPG visual

### Fase 3 (Social)
- [ ] Sistema de Guilds
- [ ] Feed de atividades
- [ ] Leaderboards
- [ ] Perfil público
- [ ] Integração Discord

### Fase 4 (Monetização)
- [ ] Assinatura Premium
- [ ] Loja Premium
- [ ] Analytics Avançados
- [ ] Vagas em Destaque
- [ ] Certificados verificados

## 10. Psicologia do Jogador

### 10.1 Tipos de Jogadores (Bartle)

**Achievers (Conquistadores):** 40%
- Motivados por badges e níveis
- Querem completar 100%
- Foco: Sistema de conquistas robusto

**Explorers (Exploradores):** 30%
- Querem descobrir features escondidas
- Gostam de badges secretas
- Foco: Easter eggs e surpresas

**Socializers (Socializadores):** 20%
- Motivados por comunidade
- Querem ajudar outros
- Foco: Code reviews e guilds

**Killers (Competidores):** 10%
- Querem ser #1 no ranking
- Competem por status
- Foco: Leaderboards e torneios

### 10.2 Loops de Engajamento

**Loop Curto (Diário):**
1. Estudar 15min
2. Ganhar XP + coins
3. Ver progresso na barra
4. Sentir satisfação
5. Voltar amanhã para streak

**Loop Médio (Semanal):**
1. Acumular coins
2. Comprar item na loja
3. Personalizar perfil
4. Mostrar para comunidade
5. Querer mais itens

**Loop Longo (Mensal):**
1. Subir de nível
2. Desbloquear novo título
3. Acessar vagas melhores
4. Conseguir entrevista
5. Compartilhar sucesso

## 11. Balanceamento Final

### 11.1 Tempo para Marcos

- **Level 10:** ~20 horas de estudo
- **Level 20:** ~80 horas de estudo
- **Level 30:** ~200 horas de estudo
- **Level 50:** ~800 horas de estudo

### 11.2 Economia Saudável

- **Inflação:** Controlada por limites de ganho diário
- **Deflação:** Evitada por itens consumíveis (Streak Freeze)
- **Sink:** Cosméticos permanentes removem coins da economia

---

**Desenvolvido com 🎮 para transformar aprendizado em vício positivo!**
