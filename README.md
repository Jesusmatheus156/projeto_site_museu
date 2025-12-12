
# 🌐 Projeto Museu na Web: Divulgação e Preservação da Cultura Indígena por Meio de um Website Interativo

Este projeto tem como objetivo desenvolver um site institucional para o Museu do Índio de Apodi/RN. A iniciativa busca valorizar a cultura indígena local e facilitar o acesso da comunidade às informações do museu, como seu acervo, eventos e história.

## 🚀 Tecnologias Utilizadas

- HTML5, CSS3, JavaScript
- Python / Django
- MySQL
- Git / GitHub

## 📦 Como Rodar o Projeto Localmente

### 1. Clone o repositório:

```bash
git clone https://github.com/Jesusmatheus156/projeto_site_museu.git
cd projeto_site_museu/projeto_museu
```
### 2. Crie e ative um ambiente virtual:

```bash
python -m venv 'nome_da_venv'
source venv/bin/activate  # para Linux/macOS
venv\Scripts\activate     # para Windows
```

### 3. Instale as dependências

```bash

pip install -r requirements.txt

```

### 4. Configure o banco de dados

Abra o arquivo projeto_museu/settings.py e edite a parte de DATABASES com os seus dados do MySQL: 
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nome_do_banco',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
### 5. Rode as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crie um superusuário para acessar o admin (opcional)
```bash
python manage.py createsuperuser
```
### 7. Rode o servidor
```bash
python manage.py runserver
```
Depois, abra o navegador no seguinte endereço:
http://127.0.0.1:8000

## Estrutura do Projeto

PROJECT_MUSEU/
├── base/        <-- app base
│   ├── static/
│   │   └── base/
│   │       └── css/
│   │       └── img/
│   │       └── js/
│   ├── templates/
│   │   └── base/
│   │       └── acervo.html
│   │       └── base.html
│   │       └── CHCTPLA.html
│   │       └── home.html
│   │       └── museu.html
│   │       └── visitar.html
│   ├── _init_.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
├── projeto_museu/ <--projeto django
│   │   └── _pycache_/
│   ├── _init_.py
│   ├── asgi.py
│   ├── settings.py
│   ├── wsgi.py
├── usuario/ <-- app usuario
│   │   └── _pycache_/
│   │   └── migrations/
│   │   └── static/
│   │       └── usuario
│   │   │       └── css/
│   │   │       └── img/
│   ├── templates/
│   │       └── usuario
│   │   │       └── agendarvisitar.html
│   ├── admin.py
│   ├── apps.py      
│   └── models.py
│   └── tests.py
│   └── urls.py
│   └── views.py
└── manage.py
└── README.md
└── requirements.txt