from io import BytesIO
from uuid import UUID

from fastapi import File, Depends, APIRouter, UploadFile, BackgroundTasks

from src.task.domain.dtos import TaskReadDTO, TaskCreateDTO
from src.task.api.dependencies import TaskUoWDepend, TaskRunnerDepend, AccountTokenDepend
from src.task.application.use_cases.get_task import GetTaskUseCase
from src.task.application.use_cases.run_task import RunTaskUseCase
from src.task.application.use_cases.create_task import CreateTaskUseCase

router = APIRouter()


@router.post("", response_model=TaskReadDTO)
async def create_and_run_task(
    uow: TaskUoWDepend,
    runner: TaskRunnerDepend,
    account_token: AccountTokenDepend,
    background_tasks: BackgroundTasks,
    data: TaskCreateDTO = Depends(TaskCreateDTO.as_form),
    image: UploadFile | None = File(None),
):
    task = await CreateTaskUseCase(uow).execute(data)
    image_buffer = None
    if image is not None:
        image_buffer = BytesIO(await image.read())
    background_tasks.add_task(RunTaskUseCase(uow, runner, account_token).execute, task.id, data, image_buffer)
    return task


@router.get("/{task_id}", response_model=TaskReadDTO)
async def get_task(task_id: UUID, uow: TaskUoWDepend):
    return await GetTaskUseCase(uow).execute(task_id)
