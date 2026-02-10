Cliniclick

Sistema web de agendamentos clínicos feito com Django 5, SQLite e Bootstrap. Inclui cadastro de usuários com modelo customizado, fluxo de agendamento de consultas e exames com prevenção de conflitos, filtros dinâmicos por especialidade e controle de sessão por inatividade.

Visão geral

Stack: Django 5, Python 3.11+, SQLite (dev), Bootstrap.

Apps: base, usuarios (usuário customizado), agenda (consultas/exames).

Objetivo: projeto “rodável em outra máquina” com documentação e dependências versionadas.

Funcionalidades

Usuário customizado usuarios.Usuario com campos extras: cep, rua, numero, complemento, bairro, cidade, estado, telefone, cpf, data_nascimento, plano_saude, apelido.

Cadastro e autenticação (login/logout).

Agenda

Modelos: Especialidade, Medico, ExameTipo, Agendamento.

Agendamento de consulta e exame com intervalos de 30 min.

Prevenção de conflitos (não permite horários sobrepostos para o mesmo médico/sala).

Filtro dinâmico de médicos por especialidade via AJAX.

Sessão / Inatividade

Popup de aviso após 10s de inatividade; 30s de contagem; expira e faz logout automático.

UI

Formulários em duas colunas.

Cartão “Preencha seus dados” ajustado ao conteúdo, com menor espaçamento interno e entre colunas (sem alterar o tamanho dos campos).

Estrutura (sugerida)

Observação: os apps podem estar na pasta apps/ ou na raiz do repositório. Adapte os caminhos conforme seu projeto.

cliniclick/
├─ manage.py
├─ requirements.txt
├─ .env.example
├─ main/                 # projeto raiz (settings/urls/asgi/wsgi)
│  ├─ settings.py
│  ├─ urls.py
│  └─ ...
├─ apps/                 # (opcional) diretório para apps
│  ├─ base/
│  ├─ usuarios/
│  └─ agenda/
├─ templates/            # templates globais (ex.: base/base.html, index.html)
└─ static/               # css, js, imagens

🔧 Pré‑requisitos

Python 3.11+

Pip e Virtualenv

Rodando localmente

# 1) Clonar e entrar no projeto
git clone <URL_DO_REPO>
cd cliniclick

# 2) Criar e ativar o ambiente virtual
python -m venv venv
# Windows (CMD):
venv\Scripts\activate
# Windows (PowerShell):
.\venv\Scripts\Activate
# Linux/macOS:
source venv/bin/activate

# 3) Instalar dependências
pip install -r requirements.txt  # (ou veja a seção de requirements)

# 4) Variáveis de ambiente
cp .env.example .env             # edite conforme necessário

# 5) Migrar o banco
python manage.py migrate

# 6) Criar superusuário
python manage.py createsuperuser

# 7) Subir o servidor
python manage.py runserver

Configuração do Django (exemplo)

# main/settings.py (trechos úteis)
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-secret')
DEBUG = os.getenv('DEBUG', '1') == '1'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    # Apps do projeto (ajuste o caminho conforme sua estrutura)
    'apps.base', 'apps.usuarios', 'apps.agenda',
]

AUTH_USER_MODEL = 'usuarios.Usuario'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],  # garante que index.html fora de main seja achado
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

Dica para 404 na raiz: crie uma rota para "/" em main/urls.py apontando para index.

# main/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('usuarios/', include('apps.usuarios.urls')),
    path('agenda/', include('apps.agenda.urls')),
]

Variáveis de ambiente (.env.example)

DJANGO_SECRET_KEY=troque-por-uma-chave-segura
DEBUG=1
ALLOWED_HOSTS=127.0.0.1,localhost
SESSION_IDLE_POPUP_SECONDS=10
SESSION_IDLE_COUNTDOWN=30

Modelos / Fluxos principais

usuarios

Modelo: Usuario (custom user) + campos extras listados acima.

Páginas: cadastro, login, perfil.

Formulário de cadastro: layout em duas colunas, caixa do card ajustada ao conteúdo, gap reduzido entre colunas.

agenda

Modelos:

Especialidade(nome)

Medico(nome, especialidade, crm, ... )

ExameTipo(nome, preparo, ... )

Agendamento(tipo, medico, paciente, data, hora, duração=30min, status, ... )

Regras:

Intervalos de 30 minutos.

Bloqueio de conflitos de horário para o mesmo médico/sala.

Filtro AJAX: ao escolher a especialidade, a lista de médicos é atualizada sem recarregar a página.

Sessão / Inatividade

JS monitora inatividade; após 10s abre popup com 30s de contagem e encerra a sessão.

URLs (exemplos)

/ → index.html

/admin/ → Django Admin

/usuarios/cadastro/, /usuarios/login/, /usuarios/perfil/

/agenda/agendar/, /agenda/listar/, /agenda/editar/<id>/, /agenda/excluir/<id>/

Ajuste conforme seus urls.py de cada app.

Requisitos (requirements)

Gerar/atualizar requirements.txt com o venv ativo:

pip freeze > requirements.txt

Instalar depois:

pip install -r requirements.txt

Alternativas úteis:

# pip-tools - compilar a partir de requirements.in
pip install pip-tools
pip-compile -o requirements.txt

# pipreqs - gerar a partir dos imports do código
pip install pipreqs
pipreqs . --force

Testes (sugestão)

python manage.py test

Adicione testes de validação de conflito de agenda e do filtro AJAX.

Deploy (pontos de atenção)

Defina DEBUG=0 e ALLOWED_HOSTS adequados.

Configure SECRET_KEY seguro.

Use Postgres/MySQL no ambiente produtivo.

Configure STATIC_ROOT e rode collectstatic.

Solução de problemas

404 na raiz: inclua rota '' em main/urls.py apontando para index.html.

Templates não encontrados: garanta TEMPLATES['DIRS'] = [BASE_DIR / 'templates'].

Apps em apps/: use import com caminho completo em INSTALLED_APPS (ex.: 'apps.agenda').

Changelog recente

Cadastro (UI):

Manter duas colunas.

Caixa “Preencha seus dados” agora acompanha o tamanho dos campos, com padding/gaps menores e aparência mais compacta.

Redução do espaço entre a primeira e a segunda coluna.

Agenda:

Regras de 30 min e bloqueio de conflitos implementadas/ajustadas.

Filtro AJAX de médicos por especialidade.

Sessão: popup de inatividade (10s) + contagem de 30s para auto-logout.

Docs: este README criado/atualizado; incluídas instruções de requirements.txt.

Dicas Git rápidas

Desfazer o último commit mantendo as alterações no working tree:

git reset --soft HEAD~1

Desfazer o git add . (tirar do stage):

git restore --staged .

Reverter um commit já enviado (gera novo commit de reversão):

git revert <hash>

Roadmap

Documentação dos endpoints da agenda (API opcional).

Testes automatizados para conflitos de horário.

Deploy (Docker + Postgres) e CI/CD.

Port para Android (app cliente) após estabilização do backend.
