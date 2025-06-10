from fastapi import FastAPI
from sqladmin import Admin

from src.db.engine import engine
from src.core.admin import authentication_backend
from src.core.config import settings
from src.task.api.rest import router as task_router
from src.task.api.admin import TaskAdmin
from src.account.api.admin import AccountAdmin
from src.core.logging_setup import setup_fastapi_logging
from src.integration.api.rest import router as integration_router

app = FastAPI(title=settings.PROJECT_NAME)
setup_fastapi_logging(app)


app.include_router(task_router, prefix="/api/task", tags=["Task"])
app.include_router(integration_router, prefix="/api/integration", tags=["Integration"])


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(AccountAdmin)
admin.add_view(TaskAdmin)
