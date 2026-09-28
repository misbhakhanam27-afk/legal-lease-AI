from typing import Optional

from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_type: str = Field(
        ...,
        min_length=2,
        description="Type of legal document"
    )

    parties: str = Field(
        ...,
        min_length=2,
        description="Names and details of the parties"
    )

    terms: str = Field(
        ...,
        min_length=2,
        description="Main terms and conditions"
    )

    effective_date: str = Field(
        ...,
        min_length=2,
        description="Effective date of the document"
    )

    jurisdiction: Optional[str] = ""

    additional_instructions: Optional[str] = ""


class DocumentResponse(BaseModel):
    success: bool
    document_type: str
    content: str
    message: str
