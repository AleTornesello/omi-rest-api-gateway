from decimal import Decimal
from enum import StrEnum

from pydantic import Field

from omi_rest_api_gateway.schemas.common import ApiModel


class ContractType(StrEnum):
    sale = "sale"
    rent = "rent"


class OmiQuotationQuery(ApiModel):
    province: str | None = Field(default=None, min_length=2, max_length=2)
    municipality: str | None = None
    zone: str | None = None
    semester: str | None = Field(default=None, pattern=r"^\d{4}-[12]$")
    property_type: str | None = None
    contract_type: ContractType | None = None


class ValueRange(ApiModel):
    min: Decimal | None = None
    max: Decimal | None = None
    unit: str


class OmiQuotation(ApiModel):
    zone: str
    description: str | None = None
    property_type: str
    market_value: ValueRange | None = None
    rental_value: ValueRange | None = None


class OmiQuotationSearchResponse(ApiModel):
    source: str = "Agenzia Entrate - OMI"
    query: OmiQuotationQuery
    results: list[OmiQuotation]
