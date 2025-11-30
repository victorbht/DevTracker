# DevTracker - Guia de Deploy

## 🐳 Docker (Recomendado)

### **Quick Start**

```bash
# Copiar variáveis de ambiente
cp .env.example .env

# Editar .env com suas configurações
nano .env

# Subir containers
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Parar containers
docker-compose down
```

### **Produção com Docker**

```bash
# Build para produção
docker build -t devtracker:latest .

# Run com variáveis de ambiente
docker run -d \
  -p 8000:8000 \
  -e DJANGO_SECRET_KEY="your-secret" \
  -e DATABASE_URL="postgresql://..." \
  -e DJANGO_DEBUG=False \
  devtracker:latest
```

---

## 🚀 Preparação para Produção

### **1. Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto:

```bash
# Django
DJANGO_SECRET_KEY=sua-chave-secreta-aqui-use-python-secrets
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=seudominio.com,www.seudominio.com

# Database (PostgreSQL em produção)
DATABASE_URL=postgresql://user:password@localhost:5432/devtracker

# Opcional
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
```

### **2. Instalar Dependências de Produção**

```bash
pipenv install gunicorn psycopg2-binary whitenoise
```

### **3. Configurar settings.py para Produção**

```python
# devtracker/settings.py

import os
from pathlib import Path
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Database
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files (WhiteNoise)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Adicionar
    # ... resto do middleware
]

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
```

---

## 🐳 Deploy com Docker

### **Dockerfile**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Instalar pipenv
RUN pip install pipenv

# Copiar arquivos de dependências
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

# Copiar projeto
COPY . .

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

# Expor porta
EXPOSE 8000

# Comando de inicialização
CMD ["gunicorn", "devtracker.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### **docker-compose.yml**

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: devtracker
      POSTGRES_USER: devtracker
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    
  web:
    build: .
    command: gunicorn devtracker.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

volumes:
  postgres_data:
  static_volume:
```

### **Comandos Docker**

```bash
# Build
docker-compose build

# Rodar migrações
docker-compose run web python manage.py migrate

# Criar superuser
docker-compose run web python manage.py createsuperuser

# Popular badges
docker-compose run web python manage.py seed_badges

# Iniciar
docker-compose up -d
```

---

## ☁️ Deploy em Plataformas Cloud

### **Railway**

1. Instalar Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login e deploy:
```bash
railway login
railway init
railway add
railway up
```

3. Configurar variáveis de ambiente no dashboard Railway

4. Adicionar PostgreSQL:
```bash
railway add postgresql
```

### **Fly.io**

1. Instalar Fly CLI:
```bash
curl -L https://fly.io/install.sh | sh
```

2. Login e deploy:
```bash
fly auth login
fly launch
fly deploy
```

3. Configurar secrets:
```bash
fly secrets set DJANGO_SECRET_KEY=sua-chave
fly secrets set DJANGO_DEBUG=False
```

### **Render**

1. Criar `render.yaml`:
```yaml
services:
  - type: web
    name: devtracker
    env: python
    buildCommand: "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate"
    startCommand: "gunicorn devtracker.wsgi:application"
    envVars:
      - key: DJANGO_SECRET_KEY
        generateValue: true
      - key: DJANGO_DEBUG
        value: False
      - key: DATABASE_URL
        fromDatabase:
          name: devtracker-db
          property: connectionString

databases:
  - name: devtracker-db
    plan: free
```

2. Conectar repositório GitHub no dashboard Render

---

## 📋 Checklist Pré-Deploy

- [ ] Variáveis de ambiente configuradas
- [ ] `DEBUG=False` em produção
- [ ] `ALLOWED_HOSTS` configurado
- [ ] Banco de dados PostgreSQL configurado
- [ ] Migrações aplicadas
- [ ] Arquivos estáticos coletados
- [ ] Superuser criado
- [ ] Badges populadas (`seed_badges`)
- [ ] HTTPS configurado
- [ ] Backup automático configurado

---

## 🔒 Segurança

### **Gerar SECRET_KEY**

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### **Configurar CORS (se necessário)**

```bash
pipenv install django-cors-headers
```

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

CORS_ALLOWED_ORIGINS = [
    "https://seudominio.com",
]
```

---

## 📊 Monitoramento

### **Logs**

```bash
# Docker
docker-compose logs -f web

# Railway
railway logs

# Fly.io
fly logs
```

### **Health Check**

Adicionar endpoint de health check:

```python
# core/views.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'ok'})

# core/urls.py
urlpatterns = [
    path('health/', views.health_check, name='health'),
    # ...
]
```

---

## 🎯 Pós-Deploy

1. Testar todas as funcionalidades
2. Verificar logs de erro
3. Configurar backup automático
4. Monitorar performance
5. Configurar alertas (Sentry, etc)

**DevTracker pronto para produção!** 🚀
