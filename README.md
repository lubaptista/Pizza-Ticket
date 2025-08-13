# ​ Pizza Ticket

## Sistema de Comanda para Pizzaria

Este é um sistema de comanda desenvolvido com base no módulo "Conhecendo Sistema Pizzaria" do curso Full Stack (NodeJS, React, TypeScript) da Udemy. O objetivo deste projeto é gerenciar pedidos de uma pizzaria de forma eficiente, integrando backend e frontend com uma experiência interativa e amigável.

##  Sobre o projeto

- **Backend**: Node.js com TypeScript, fornecendo API REST para gerenciamento de pedidos, itens de comanda, clientes, e produtos.
- **Frontend**: React com TypeScript, interface user-friendly para criação e acompanhamento de comandas em tempo real.
- **Propósito**: Simular um sistema real de pizzaria, onde é possível criar comandas, adicionar pizzas, bebidas, editá-las, visualizar o status dos pedidos, etc.

##  Funcionalidades principais

- Autenticação básica (opcional)
- Criar nova comanda
- Adicionar, editar e remover itens (pizza, bebida, observações)
- Visualizar lista de comandas em aberto e finalizadas
- Atualizar status de comanda (em preparo, pronta, entregue)
- Integração entre frontend e backend via API REST

##  Tecnologias

### Backend
- Node.js
- TypeScript
- Express (ou framework similar)
- Banco de dados (ex: MongoDB, PostgreSQL, MySQL)
- ORM ou driver (Mongoose, Prisma, TypeORM etc.)
- JWT (para autenticação, se aplicável)

### Frontend
- React com TypeScript
- React Router (navegação entre telas)
- Axios ou Fetch para requisições API
- Componentes funcionais, hooks, estados e context API

##  Estrutura de pastas (exemplo)
```bash
backend/
│── src/
│ ├── controllers/
│ ├── models/
│ ├── routes/
│ └── index.ts
frontend/
│── src/
│ ├── components/
│ ├── pages/
│ ├── services/
│ └── App.tsx
.gitignore
```

##  Instruções de instalação

### Backend:

Entre na pasta do backend:
```bash
cd backend
```

Instale as dependências:
```bash
npm install
```

Rode o programa(backend):
```bash
npm run dev
```

<!-- ### Frontend

Entre na pasta do frontend:
```bash
cd frontend
```

Instale as dependências:
```bash
npm install
```

Rode o programa(frontend):
```bash
npm start
```
-->

### Crie um .env com 

```bash
git clone https://github.com/seu-usuario/nome-do-projeto.git
cd nome-do-projeto
```