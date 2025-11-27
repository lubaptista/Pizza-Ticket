# Dockerfile
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /usr/src/app

# Copia o arquivo de dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# CORREÇÃO: Copia a pasta backend inteira, que agora contém __init__.py
# Isso permite que importações como 'from backend.models import db' funcionem.
COPY backend/ backend/ 
COPY test_backend.py .

# Comando para rodar a aplicação 
CMD ["python", "backend/app.py"] # CORREÇÃO: Altera o comando para rodar o app de dentro da pasta