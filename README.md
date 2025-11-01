
# 🌐 Projeto Website do Museu do Indígena Luiza Cantofa de Apodi/RN

Este projeto tem como objetivo desenvolver um site institucional para o Museu do Índio de Apodi/RN. A iniciativa busca valorizar a cultura indígena local e facilitar o acesso da comunidade às informações do museu, como seu acervo, eventos e história.

## 🚀 Tecnologias Utilizadas

- HTML5, CSS3, JavaScript
- Python / Django
- MySQL
- Bootstrap
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
