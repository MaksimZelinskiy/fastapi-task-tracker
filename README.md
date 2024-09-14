# FASTAPI Таск трекер
### Tech stack

- **PL**: Python
- **Framework**: FastAPI
- **DB**: PostgreSQL
- **Documentation  API**: Built-in FastAPI documentation is available at `/docs`.
- **Tests**: pytest 

## Project structure:
```
project/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py
│   │   ├── user.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── tasks.py
│   │   ├── auth.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py
│   │   ├── user.py
│   ├── config/
│   │   ├── __init__.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── email_sender.py
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Setup and installation

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/MaksimZelinskiy/fastapi-task-tracker.git
   cd fastapi-task-tracker/
   ```
2. Build and run Docker containers:
   ```bash
   docker-compose up --build
   ```
3. The API will be available at `http://localhost:8000`.

#### Documentation API
- Documentation API: `http://localhost:8000/docs`.



