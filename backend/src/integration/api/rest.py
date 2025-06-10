from fastapi import APIRouter

router = APIRouter()


@router.get("/higgsfield/motions")
async def get_motions_list():
    raise NotImplementedError()
