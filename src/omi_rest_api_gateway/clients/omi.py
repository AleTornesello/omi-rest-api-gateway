import httpx

from omi_rest_api_gateway.schemas.omi import OmiQuotationQuery


class OmiPortalClient:
    """HTTP client boundary for the upstream Agenzia Entrate OMI portal."""

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self._http_client = http_client

    async def fetch_quotations(self, query: OmiQuotationQuery) -> list[dict[str, object]]:
        # TODO: map this method to the real OMI portal search flow.
        # Keeping the client boundary in place makes endpoint tests independent from upstream I/O.
        _ = query
        return []
