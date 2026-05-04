from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from omi_rest_api_gateway.dependencies import get_omi_service
from omi_rest_api_gateway.schemas.omi import (
    ContractType,
    OmiQuotationQuery,
    OmiQuotationSearchResponse,
)
from omi_rest_api_gateway.services.omi import OmiService

router = APIRouter()


@router.get(
    "/quotations",
    response_model=OmiQuotationSearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Search OMI quotations",
)
async def search_quotations(
    service: Annotated[OmiService, Depends(get_omi_service)],
    province: Annotated[
        str | None,
        Query(min_length=2, max_length=2, description="Italian province code, for example MI."),
    ] = None,
    municipality: Annotated[
        str | None,
        Query(min_length=1, description="Italian municipality name."),
    ] = None,
    zone: Annotated[
        str | None,
        Query(min_length=1, description="OMI territorial zone code."),
    ] = None,
    semester: Annotated[
        str | None,
        Query(pattern=r"^\d{4}-[12]$", description="Reference semester, for example 2025-2."),
    ] = None,
    property_type: Annotated[
        str | None,
        Query(alias="propertyType", min_length=1, description="OMI property category."),
    ] = None,
    contract_type: Annotated[
        ContractType | None,
        Query(alias="contractType", description="Quotation contract type."),
    ] = None,
) -> OmiQuotationSearchResponse:
    query = OmiQuotationQuery(
        province=province,
        municipality=municipality,
        zone=zone,
        semester=semester,
        property_type=property_type,
        contract_type=contract_type,
    )
    return await service.search_quotations(query)
