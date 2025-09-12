# 🍕 Sistema de Comandas para Pizzaria

Este projeto é uma aplicação **Fullstack** para gerenciamento de comandas em uma pizzaria.  
Permite o cadastro de pedidos, controle de status (aberto, em preparo, entregue) e autenticação de usuários com diferentes perfis.

---

## 🎯 Objetivos do Sistema

- 📋 Criar e gerenciar comandas
- 🍽️ Associar pedidos de pizzas e bebidas a cada comanda
- 🔐 Autenticação de usuários com perfis diferentes:
  - **Garçom** → abre comandas e envia pedidos
  - **Cozinha** → visualiza pedidos e atualiza status

---

## ⚙️ Tecnologias Utilizadas

### Backend
- Python 3.10+
- FastAPI
- JWT (PyJWT)
- SQLAlchemy
- Banco de dados: PostgreSQL (pode usar SQLite para testes)

### Frontend
- React 18
- Vite
- React Router DOM
- Axios
- TailwindCSS

---

## 🚀 Como rodar o projeto

### 🔹 Backend

1. Clone o repositório:
    ```bash
        git clone https://github.com/seu-usuario/pizzaria-comandas.git
        cd pizzaria-comandas/backend
    ```

2. Crie e ative um ambiente virtual:
    ```bash
        python -m venv venv
        source venv/bin/activate   # Linux/Mac
        venv\Scripts\activate      # Windows
    ```

3. Instale as dependências:
    ```bash
        pip install -r requirements.txt
    ```

4. Execute o servidor:
    ```bash
        flask run --host=0.0.0.0 --port=5000
    ```
<!-- uvicorn main:app --reload -->
O backend estará rodando em: http://192.168.56.30:5000

### 🔹 Frontend

1. Vá para a pasta frontend:
    ```bash
        cd ../frontend
    ```
    
2. Instale as dependências:
    ```bash
        npm install
    ```

3. Rode o projeto:
    ```bash
        npm run dev -- --host
    ```

O frontend estará disponível em: http://192.168.56.20:5173

### 🔹 Nginx

1. Instale o Nginx dentro da Vm1:
    ```bash
        sudo apt install nginx -y
    ```
    
2. Configure o nginx:
    ```bash
        sudo nano /etc/nginx/sites-available/default
    ```

3. Coloque esse codigo:
    ```bash
        server {
                listen 80 default_server;
                listen [::]:80 default_server;
            
                server_name pizzaticket;
            
                location / {
                    proxy_pass http://192.168.56.20:5173/; # IP da VM Frontend
            
                    proxy_http_version 1.1;
                    proxy_set_header Upgrade $http_upgrade;
                    proxy_set_header Connection 'upgrade';
                    proxy_set_header Host $host;
                    proxy_cache_bypass $http_upgrade;
                }
    
          location /api/ {
              rewrite ^/api/(.*) /$1 break; # Esta linha remove o /api
          
              proxy_pass http://192.168.56.30:5000;
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              proxy_connect_timeout 60s;
              proxy_send_timeout 60s;
              proxy_read_timeout 60s;
          
              # CORS
              add_header Access-Control-Allow-Origin *;
              add_header Access-Control-Allow-Methods 'GET, POST, PUT, DELETE, OPTIONS';
              add_header Access-Control-Allow-Headers "Authorization, Content-Type";
          
              if ($request_method = 'OPTIONS') {
                  return 204;
              }
          }
        }
    ```
    
4. Execute o Nginx:
    ```bash
        sudo systemctl start nginx
    ```

5. Parar o nginx:
    ```bash
        sudo systemctl stop nginx
    ```
# Aviso

Tanto o frontend quanto o backend não irão aparecer os Ip correspondentes a eles e sim o Ip Nat do Proxy que é 192.168.91.143 
