# 🎮 Guia de Migração - Pacote Gamer

## Passo a Passo para Ativar o Pacote Gamer

### 1. Criar e Aplicar Migrações

```bash
# Gerar arquivos de migração
python manage.py makemigrations

# Aplicar migrações ao banco de dados
python manage.py migrate
```

**Saída esperada:**
```
Migrations for 'core':
  core/migrations/0007_skillnode_perfilgamer_sessaogamer_itemloja_inventariousuario_questemprego_bossbattle_submissaoprojeto_codereview.py
    - Create model SkillNode
    - Create model PerfilGamer
    - Create model SessaoGamer
    - Create model ItemLoja
    - Create model InventarioUsuario
    - Create model QuestEmprego
    - Create model BossBattle
    - Create model SubmissaoProjeto
    - Create model CodeReview
```

### 2. Popular Dados Iniciais

```bash
# Popular skill tree, loja e boss battles
python manage.py seed_gamer_pack
```

**Isso criará:**
- ✅ 10 skills (Python, Django, React, Node.js, etc.)
- ✅ 6 itens cosméticos (molduras e banners)
- ✅ 4 boss battles (Fácil → Lendário)

### 3. Criar Perfis Gamer para Usuários Existentes

Se você já tem usuários cadastrados, execute no shell do Django:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from core.models import PerfilGamer, InventarioUsuario

# Criar perfis para todos os usuários
for user in User.objects.all():
    PerfilGamer.objects.get_or_create(user=user)
    InventarioUsuario.objects.get_or_create(user=user)
    print(f"✅ Perfil criado para {user.username}")

exit()
```

### 4. Verificar no Admin

Acesse o Django Admin: `http://localhost:8000/admin/`

Você verá as novas seções:
- **GAMIFICAÇÃO ORIGINAL**
  - Conquistas
  - Perfis de Usuário
  
- **PACOTE GAMER**
  - Skill Nodes (Árvore de Habilidades)
  - Perfis Gamer
  - Sessões Gamer
  - Itens da Loja
  - Inventários
  - Quests de Emprego
  - Boss Battles
  - Submissões de Projetos
  - Code Reviews

### 5. Testar o Sistema

```bash
# Rodar testes do Pacote Gamer
pytest core/tests/test_gamer_pack.py -v

# Rodar todos os testes
pytest
```

## Compatibilidade com Sistema Existente

O Pacote Gamer foi projetado para **coexistir** com o sistema original:

### Sistema Original (Mantido)
- ✅ `SessaoEstudo` → Continua funcionando normalmente
- ✅ `PerfilUsuario` → Sistema de XP/conquistas original
- ✅ `Tecnologia` e `MetodoEstudo` → Não afetados

### Sistema Novo (Adicional)
- 🆕 `SessaoGamer` → Sessões com multiplicadores de XP
- 🆕 `PerfilGamer` → Sistema RPG avançado
- 🆕 `SkillNode` → Árvore de habilidades hierárquica

### Relacionamentos
```
User
├── perfil (PerfilUsuario) ← Sistema Original
└── perfil_gamer (PerfilGamer) ← Pacote Gamer
    ├── inventario (InventarioUsuario)
    ├── skills_desbloqueadas (SkillNode)
    ├── equipped_frame (ItemLoja)
    └── equipped_banner (ItemLoja)
```

## Migração Gradual (Opcional)

Se quiser migrar dados do sistema antigo para o novo:

```python
from core.models import SessaoEstudo, SessaoGamer, Tecnologia, SkillNode
from django.contrib.auth.models import User

# Exemplo: Migrar sessões antigas para o novo formato
for sessao_antiga in SessaoEstudo.objects.all():
    # Encontrar ou criar skill correspondente
    skill, _ = SkillNode.objects.get_or_create(
        nome=sessao_antiga.tecnologia.nome,
        defaults={'icone_fa': 'fas fa-code'}
    )
    
    # Mapear método antigo para novo
    metodo_map = {
        'Video': 'VIDEO',
        'Leitura': 'READING',
        'Prática': 'CODING',
        'Projeto': 'PROJECT',
    }
    
    metodo_novo = metodo_map.get(sessao_antiga.metodo.nome, 'VIDEO')
    
    # Criar sessão gamer
    SessaoGamer.objects.create(
        user=User.objects.first(),  # Ajustar conforme necessário
        skill=skill,
        inicio=sessao_antiga.data_registro,
        fim=sessao_antiga.data_registro + sessao_antiga.tempo_liquido,
        metodo=metodo_novo,
        descricao=sessao_antiga.topico
    )
```

## Rollback (Se Necessário)

Se precisar reverter as mudanças:

```bash
# Reverter para migração anterior
python manage.py migrate core 0006_perfilusuario_meta_mensal_perfilusuario_meta_semanal

# Remover arquivos de migração
rm core/migrations/0007_*.py
```

## Troubleshooting

### Erro: "No such table: core_perfilgamer"
**Solução:** Execute `python manage.py migrate`

### Erro: "UNIQUE constraint failed"
**Solução:** Limpe dados duplicados antes de migrar
```python
from core.models import PerfilGamer
# Remover perfis duplicados
for user in User.objects.all():
    perfis = PerfilGamer.objects.filter(user=user)
    if perfis.count() > 1:
        perfis.exclude(id=perfis.first().id).delete()
```

### Erro: "ImportError: cannot import name 'slugify'"
**Solução:** Já está importado no models.py, mas se persistir:
```python
from django.utils.text import slugify
```

## Próximos Passos

Após a migração bem-sucedida:

1. **Criar Views e Templates**
   - [ ] Página da Skill Tree
   - [ ] Loja de Cosméticos
   - [ ] Boss Battles
   - [ ] Code Review System

2. **Integrar com Dashboard**
   - [ ] Widget de Level/XP no header
   - [ ] Notificações de level up
   - [ ] Barra de progresso de XP

3. **Adicionar Funcionalidades**
   - [ ] Sistema de compra na loja
   - [ ] Submissão de projetos
   - [ ] Code review entre usuários
   - [ ] Leaderboards

## Suporte

Dúvidas ou problemas? Consulte:
- [PACOTE_GAMER.md](PACOTE_GAMER.md) - Documentação completa
- [core/tests/test_gamer_pack.py](core/tests/test_gamer_pack.py) - Exemplos de uso

---

**Boa sorte e bom jogo! 🎮🚀**
