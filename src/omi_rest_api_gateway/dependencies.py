from typing import cast

from fastapi import Request

from omi_rest_api_gateway.clients.omi import OmiPortalClient
from omi_rest_api_gateway.services.omi import OmiService


def get_omi_client(request: Request) -> OmiPortalClient:
    return cast(OmiPortalClient, request.app.state.omi_client)


def get_omi_service(request: Request) -> OmiService:
    return OmiService(client=get_omi_client(request))
