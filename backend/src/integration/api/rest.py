from fastapi import APIRouter, Depends

from src.integration.api.dependencies import ExternalClientDepend
from src.integration.application.use_cases.get_higgsfield_motions import GetHiggsfieldMotionsUseCase
from src.integration.domain.dtos import IntegrationHiggsfieldMotionDTO, IntegrationHiggsfieldMotionRequestDTO

router = APIRouter()


@router.get("/higgsfield/motions", response_model=list[IntegrationHiggsfieldMotionDTO])
async def get_motions_list(
    external_client: ExternalClientDepend, params: IntegrationHiggsfieldMotionRequestDTO = Depends()
):
    return await GetHiggsfieldMotionsUseCase(external_client).execute(params)
