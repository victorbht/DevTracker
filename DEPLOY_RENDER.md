# Deploy no Render - Passo a Passo

## 📋 Pré-requisitos
- Conta no Render (https://render.com)
- Repositório GitHub público ou privado conectado

## 🚀 Passos para Deploy

### 1. Criar Conta no Render
- Acesse https://render.com
- Faça login com GitHub

### 2. Criar PostgreSQL Database
1. No dashboard, clique em **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `devtracker-db`
   - **Database**: `devtracker`
   - **User**: `devtracker`
   - **Region**: escolha a mais próxima
   - **Plan**: Free
3. Clique em **"Create Database"**
4. Aguarde a criação (1-2 minutos)
5. **Copie a "Internal Database URL"** (vamos usar depois)

### 3. Criar Web Service
1. No dashboard, clique em **"New +"** → **"Web Service"**
2. Conecte seu repositório GitHub: `victorbht/DevTracker`
3. Configure:
   - **Name**: `devtracker`
   - **Region**: mesma do banco
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn devtracker.wsgi:application`
   - **Plan**: Free

### 4. Configurar Environment Variables
Na seção **"Environment"**, adicione:

```
PYTHON_VERSION=3.12.0
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<clique em "Generate" para gerar automaticamente>
DATABASE_URL=<cole a Internal Database URL do passo 2>
```

### 5. Deploy
1. Clique em **"Create Web Service"**
2. Aguarde o build (5-10 minutos na primeira vez)
3. Acompanhe os logs em tempo real

### 6. Criar Superusuário
Após o deploy bem-sucedido:

1. No dashboard do seu web service, vá em **"Shell"**
2. Execute:
```bash
python manage.py createsuperuser
```
3. Siga as instruções para criar usuário admin

### 7. Acessar Aplicação
- URL: `https://devtracker.onrender.com` (ou o nome que você escolheu)
- Admin: `https://devtracker.onrender.com/admin`

## 🔧 Troubleshooting

### Build falhou?
- Verifique os logs no dashboard
- Confirme que `requirements.txt` está atualizado
- Verifique se `build.sh` tem permissão de execução

### Erro de static files?
```bash
# No Shell do Render
python manage.py collectstatic --noinput
```

### Erro de database?
- Confirme que DATABASE_URL está correto
- Verifique se o banco foi criado na mesma região

### Aplicação não inicia?
- Verifique se DJANGO_SECRET_KEY está configurado
- Confirme que DJANGO_DEBUG=False
- Veja os logs para erros específicos

## 📊 Monitoramento

### Logs
- Acesse **"Logs"** no dashboard do web service
- Logs em tempo real de todas as requisições

### Métricas
- CPU, memória e bandwidth no dashboard
- Plano Free: 750 horas/mês

## 🔄 Atualizações

### Deploy automático
- Cada push para `main` dispara novo deploy automaticamente
- Acompanhe o progresso em **"Events"**

### Deploy manual
- No dashboard, clique em **"Manual Deploy"** → **"Deploy latest commit"**

## 💰 Custos

### Plano Free
- ✅ 750 horas/mês
- ✅ PostgreSQL 256MB
- ✅ SSL automático
- ⚠️ Aplicação hiberna após 15min de inatividade
- ⚠️ Cold start de ~30s

### Upgrade para Paid
- $7/mês por serviço
- Sem hibernação
- Mais recursos

## 🎯 Próximos Passos

1. ✅ Testar todas as funcionalidades
2. ✅ Criar usuário admin
3. ✅ Popular badges iniciais
4. ✅ Configurar domínio customizado (opcional)
5. ✅ Configurar monitoramento (Sentry, etc)

**DevTracker no ar! 🚀**
