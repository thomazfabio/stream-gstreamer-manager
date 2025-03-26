app-fastapi/
│
├── app/
│   ├── __init__.py            # Inicializa o app e os pacotes
│   ├── main.py                # Arquivo principal que executa o FastAPI
│   ├── routes/                # Pacote para as rotas
│   │   ├── __init__.py        # Registra as rotas no app principal
│   │   └── user_routes.py     # Rotas relacionadas aos usuários
│   │
│   ├── models/                # Pacote para os modelos Pydantic ou SQLAlchemy
│   │   ├── __init__.py        # Pode importar os modelos aqui
│   │   └── user_model.py      # Modelo de usuário (Pydantic ou SQLAlchemy)
│   │
│   └── controllers/           # Pacote para a lógica de negócios
│       ├── __init__.py        # Inicializa os controladores
│       └── user_controller.py # Lógica para tratar dados e interagir com a DB
│
├── requirements.txt           # Dependências do projeto
└── README.md   