from src.integration.domain.dtos import IntegrationHiggsfieldMotionDTO, IntegrationHiggsfieldMotionRequestDTO
from src.integration.infrastructure.external.client import ExternalClient
from src.integration.infrastructure.external.schemas import ExternalGetMotionsRequest


class GetHiggsfieldMotionsUseCase:
    def __init__(self, external_client: ExternalClient) -> None:
        self.external_client = external_client

    async def execute(self, dto: IntegrationHiggsfieldMotionRequestDTO) -> list[IntegrationHiggsfieldMotionDTO]:
        request = ExternalGetMotionsRequest(**dto.model_dump())
        motions = await self.external_client.get_video_motions(request)
        return [
            IntegrationHiggsfieldMotionDTO(**m.model_dump())
            for m in motions.items
        ]
