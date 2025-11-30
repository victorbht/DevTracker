# Deploy no Railway - Passo a Passo

## 🚂 Por que Railway?
- ✅ $5 crédito grátis/mês (suficiente para projetos pequenos)
- ✅ PostgreSQL incluído
- ✅ Deploy automático via GitHub
- ✅ Sem hibernação
- ✅ SSL automático

## 📋 Pré-requisitos
- Conta no Railway (https://railway.app)
- Repositório GitHub: https://github.com/victorbht/DevTracker

## 🚀 Deploy em 5 Minutos

### 1. Criar Conta
- Acesse https://railway.app
- Login com GitHub

### 2. Novo Projeto
1. Click **"New Project"**
2. Selecione **"Deploy from GitHub repo"**
3. Escolha: `victorbht/DevTracker`
4. Railway detecta automaticamente que é Python/Django

### 3. Adicionar PostgreSQL
1. No projeto, click **"+ New"**
2. Selecione **"Database"** → **"Add PostgreSQL"**
3. Aguarde criação (30 segundos)

### 4. Configurar Variáveis
1. Click no serviço **"devtracker"**
2. Vá em **"Variables"**
3. Click **"+ New Variable"** e adicione:

```bash
PYTHON_VERSION=3.12.0
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<gerar com comando abaixo>
```

4. Click **"+ Add Reference"** → Selecione PostgreSQL → **"DATABASE_URL"**

### 5. Gerar SECRET_KEY
No seu terminal local:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copie e cole em `DJANGO_SECRET_KEY`

### 6. Deploy
- Railway faz deploy automaticamente!
- Acompanhe em **"Deployments"**
- Aguarde 3-5 minutos

### 7. Executar Comandos
1. Click no serviço → **"Settings"** → **"Deploy"**
2. Em **"Custom Start Command"**, adicione:
```bash
python manage.py migrate && python manage.py seed_badges && gunicorn devtracker.wsgi:application
```

### 8. Criar Superusuário
1. No serviço, vá em **"Settings"**
2. Scroll até **"Service"** → Click **"Open Shell"**
3. Execute:
```bash
python manage.py createsuperuser
```

### 9. Acessar App
- URL gerada automaticamente: `https://devtracker-production.up.railway.app`
- Ou configure domínio customizado em **"Settings"** → **"Domains"**

## 🔄 Atualizações Automáticas
- Cada push para `main` dispara deploy automático
- Rollback fácil em **"Deployments"**

## 💰 Custos
- **Free Tier**: $5 crédito/mês
- **Uso estimado**: ~$3-4/mês para app pequeno
- **Upgrade**: $5/mês por $5 de crédito adicional

## 🔧 Troubleshooting

### Build falhou?
```bash
# Verificar logs em "Deployments" → Click no deploy → "View Logs"
```

### Erro de static files?
```bash
# No Shell do Railway
python manage.py collectstatic --noinput
```

### App não inicia?
- Verifique se todas as variáveis estão configuradas
- Confirme que DATABASE_URL está conectado
- Veja logs em tempo real

## 📊 Monitoramento
- **Metrics**: CPU, RAM, Network em tempo real
- **Logs**: Logs em tempo real no dashboard
- **Alerts**: Configure em Settings

## 🎯 Vantagens vs Render
| Feature | Railway | Render Free |
|---------|---------|-------------|
| Hibernação | ❌ Não | ✅ Sim (15min) |
| Cold Start | ⚡ Instantâneo | 🐌 ~30s |
| PostgreSQL | ✅ Incluído | ✅ 256MB |
| Deploy | 🚀 3-5min | 🐌 5-10min |
| Crédito | $5/mês | 750h/mês |

**Railway é melhor para produção!** 🚂
