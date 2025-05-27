from pydantic import BaseModel
from typing import Optional, Union


class UlezResponse(BaseModel):
    """Response model for ULEZ compliance check"""
    registration: str
    compliant: bool
    make_model: Optional[str] = None
    year: Optional[int] = None
    engine_category: Optional[str] = None
    co2_emissions: Optional[Union[int, str]] = None
    charge: Optional[float] = None
    message: Optional[str] = None
