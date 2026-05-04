from omi_rest_api_gateway.clients.omi import OmiPortalClient
from omi_rest_api_gateway.schemas.omi import (
    OmiQuotation,
    OmiQuotationQuery,
    OmiQuotationSearchResponse,
)


class OmiService:
    def __init__(self, client: OmiPortalClient) -> None:
        self._client = client

    async def search_quotations(self, query: OmiQuotationQuery) -> OmiQuotationSearchResponse:
        rows = await self._client.fetch_quotations(query)
        quotations = [OmiQuotation.model_validate(row) for row in rows]
        return OmiQuotationSearchResponse(query=query, results=quotations)
