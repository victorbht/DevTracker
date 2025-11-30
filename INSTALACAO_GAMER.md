# 🎮 Instalação Rápida - Pacote Gamer

## ✅ Arquivos Criados/Modificados

### Novos Arquivos
- ✅ `core/signals.py` - Sinais para criar perfis automaticamente
- ✅ `core/management/commands/seed_gamer_pack.py` - Popular dados iniciais
- ✅ `core/tests/test_gamer_pack.py` - Testes do pacote gamer
- ✅ `PACOTE_GAMER.md` - Documentação completa
- ✅ `MIGRACAO_GAMER_PACK.md` - Guia de migração
- ✅ `INSTALACAO_GAMER.md` - Este arquivo

### Arquivos Modificados
- ✅ `core/models.py` - Adicionados 9 novos modelos
- ✅ `core/admin.py` - Registrados novos modelos no admin
- ✅ `core/apps.py` - Registrado import de signals
- ✅ `core/views.py` - Adicionadas 4 novas views
- ✅ `core/urls.py` - Adicionadas 4 novas rotas
- ✅ `core/templates/core/dashboard.html` - Atualizado para usar novos dados
- ✅ `README.md` - Documentação atualizada

## 🚀 Comandos para Ativar

```bash
# 1. Criar migrações
python manage.py makemigrations

# 2. Aplicar migrações
python manage.py migrate

# 3. Popular dados iniciais (skills, loja, bosses)
python manage.py seed_gamer_pack

# 4. Rodar testes
pytest core/tests/test_gamer_pack.py -v

# 5. Iniciar servidor
python manage.py runserver
```

## 📋 Novos Modelos Criados

1. **SkillNode** - Árvore de habilidades hierárquica
2. **PerfilGamer** - Sistema RPG avançado (level, XP, coins)
3. **SessaoGamer** - Sessões com multiplicadores de XP
4. **ItemLoja** - Cosméticos (molduras, banners, temas)
5. **InventarioUsuario** - Inventário de itens do usuário
6. **QuestEmprego** - Vagas gamificadas
7. **BossBattle** - Desafios de projeto (PBL)
8. **SubmissaoProjeto** - Tentativas de derrotar bosses
9. **CodeReview** - Sistema de ajuda cooperativa

## 🌐 Novas Rotas Disponíveis

- `/gamer/` - Dashboard RPG
- `/gamer/quests/` - Quadro de missões
- `/gamer/arena/<boss_id>/` - Arena de boss battle
- `/gamer/inventario/` - Inventário do usuário

## 🎯 Próximos Passos

### Templates Necessários (Criar)
- [ ] `core/templates/core/quests.html`
- [ ] `core/templates/core/arena.html`
- [ ] `core/templates/core/inventory.html`

### Funcionalidades a Implementar
- [ ] Formulário de registro de SessaoGamer
- [ ] Sistema de compra na loja
- [ ] Submissão de projetos para boss battles
- [ ] Interface de code review
- [ ] Skill tree visual (D3.js ou vis.js)

## 🧪 Verificar Instalação

```python
# No shell do Django
python manage.py shell

from core.models import SkillNode, PerfilGamer, BossBattle
from django.contrib.auth.models import User

# Verificar skills
print(f"Skills criadas: {SkillNode.objects.count()}")

# Verificar bosses
print(f"Bosses criados: {BossBattle.objects.count()}")

# Verificar perfil de um usuário
user = User.objects.first()
if user:
    print(f"Perfil Gamer: Level {user.perfil_gamer.level}, XP {user.perfil_gamer.total_xp}")
```

## 🐛 Troubleshooting

### Erro: "No module named 'core.signals'"
**Solução:** Certifique-se que `core/signals.py` existe

### Erro: "table core_perfilgamer already exists"
**Solução:** Execute `python manage.py migrate --fake-initial`

### Erro: "User has no attribute 'perfil_gamer'"
**Solução:** Execute no shell:
```python
from django.contrib.auth.models import User
from core.models import PerfilGamer, InventarioUsuario

for user in User.objects.all():
    PerfilGamer.objects.get_or_create(user=user)
    InventarioUsuario.objects.get_or_create(user=user)
```

## 📊 Dados Populados

Após `seed_gamer_pack`:

### Skills (10)
- Python, Django, Flask
- JavaScript, React, Node.js
- SQL, Git, Docker, AWS

### Itens da Loja (6)
- Moldura Neon Verde (500 coins)
- Moldura Cyber Azul (800 coins)
- Moldura Lendária Dourada (2000 coins)
- Banner Matrix (600 coins)
- Banner Cyberpunk (1000 coins)
- Tema Dark Neon (1500 coins)

### Boss Battles (4)
- Clone do Twitter (Médio - 1000 XP)
- API REST Completa (Médio - 800 XP)
- Dashboard Analytics (Difícil - 1500 XP)
- E-commerce Full Stack (Lendário - 3000 XP)

## 🎨 Integração com UI Existente

O Pacote Gamer **coexiste** com o sistema original:

- ✅ Sistema antigo (`SessaoEstudo`, `PerfilUsuario`) continua funcionando
- ✅ Sistema novo (`SessaoGamer`, `PerfilGamer`) adiciona funcionalidades
- ✅ Usuário tem ambos os perfis: `user.perfil` e `user.perfil_gamer`
- ✅ Pode migrar dados gradualmente ou usar ambos

## 📚 Documentação

- **Completa:** [PACOTE_GAMER.md](PACOTE_GAMER.md)
- **Migração:** [MIGRACAO_GAMER_PACK.md](MIGRACAO_GAMER_PACK.md)
- **Testes:** [core/tests/test_gamer_pack.py](core/tests/test_gamer_pack.py)

---

**Instalação concluída! Bom jogo! 🎮🚀**
