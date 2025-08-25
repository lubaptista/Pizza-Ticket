# 🍕 Sistema de Comandas para Pizzaria

Este projeto é uma aplicação **Fullstack** para gerenciamento de comandas em uma pizzaria.  
Permite o cadastro de pedidos, controle de status (aberto, em preparo, entregue) e autenticação de usuários com diferentes perfis.

---

## 🎯 Objetivos do Sistema

- 📋 Criar e gerenciar comandas
- 🍽️ Associar pedidos de pizzas e bebidas a cada comanda
- 🔐 Autenticação de usuários com perfis diferentes:
  - **Admin** → gerencia usuários e relatórios
  - **Garçom** → abre comandas e envia pedidos
  - **Cozinha** → visualiza pedidos e atualiza status
  - **Cliente** → consulta status do pedido

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

4. Configure as variáveis de ambiente em .env:
    ```bash
        DATABASE_URL=sqlite:///./pizzaria.db
        SECRET_KEY=sua_chave_jwt_segura
        ALGORITHM=HS256
        ACCESS_TOKEN_EXPIRE_MINUTES=60
    ```

5. Execute o servidor:
    ```bash
        python app.py
    ```
<!-- uvicorn main:app --reload -->
O backend estará rodando em: http://localhost:5000

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
        npm run dev
    ```

O frontend estará disponível em: http://localhost:5173