# Higgsfield API

## Запуск

Установка uv
```bash
pip install uv
```

Или через скрипт
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Download dependencies
```bash
uv sync --frozen
```

Create a virtual environment
```bash
cp example.env .env
# Edit .env with the necessary settings
```

Launch
```bash
docker compose up -d --build
```
Launch dev profile (with forwarded ports for DB and application)
```bash
docker compose --profile dev up -d --build
```

Or locally
```bash
uvx uvicorn backend.src.main:app --reload
```

## Code documentation

Main structure
```
backend
├── alembic                 Alembic files (DB migrations)
├── alembic.ini
└── src                     Modules
    ├── core                Internal settings/frequently used
    │   ├── config.py
    │   ├── admin.py
    │   └── logging_setup.py
    ├── db                  ORM settings and DB connection
    ├── integration         Module for integration with external services
    ├── main.py             Entry point
    └── task                Module for working with tasks. Launching, queuing, etc.
```

Module structure
```
task
├── api                         External data layer

│   ├── dependencies.py         Module dependencies
│   ├── admin.py                ModelView settings for sqladmin
│   └── rest.py                 FastAPI endpoints

├── application                 Business logic layer
│   ├── interfaces
│   │   ├── task_repository.py  Working with the task model in the DB
│   │   ├── task_runner.py      Interface for launching and getting the task result
│   │   └── task_uow.py         Unit of work. Facilitates working with sessions
│   └── use_cases
│       ├── create_task.py      Saving the task to the DB
│       ├── get_task.py         Getting the task from the DB
│       └── run_task.py         Launching the task (via integration)

├── domain                      Data layer
│   ├── dtos.py
│   ├── entities.py             Module domain models
│   └── mappers.py              Translating a model from one form to another

└── infrastructure              Data access layer. Interface implementation.
    └── db                      DB data access
        ├── orm.py              ORM models (sqlalchemy)
        ├── task_repository.py
        └── unit_of_work.py
```

Task workflow
1) src.task.api.rest - FastAPI POST /api/task
2) src.task.application.use_cases.create_task - Saving to the DB
3) src.task.application.use_cases.run_task - Launched in the background. Launch and wait for the result
4) src.integration.infrastructure.task_runner - Working with integration (HTTP, sending a request, getting the result)
5) src.task.application.use_cases.run_task - Saving the result (content or error) to the DB
6) src.task.api.rest - FastAPI GET /api/task/{task_id}
7) src.task.application.use_cases.get_task - Getting the task from the DB

The architecture allows for easy expansion of existing business logic, rewriting individual parts, and developing tests. I recommend strictly following it for ease of API maintenance.
