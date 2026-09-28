from fastapi import APIRouter, HTTPException

try:
    from .schemas import DocumentRequest, DocumentResponse
    from .ai_core.gemini_generator import GeminiDocumentGenerator
    from .utils.sanitizer import sanitize_text
except ImportError:  # pragma: no cover
    from schemas import DocumentRequest, DocumentResponse
    from ai_core.gemini_generator import GeminiDocumentGenerator
    from utils.sanitizer import sanitize_text


router = APIRouter()

generator = GeminiDocumentGenerator()


@router.get("/status")
def backend_status():
    return {
        "status": "online",
        "service": "LegalEase Backend"
    }


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(request: DocumentRequest):

    try:

        generated_content = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
            jurisdiction=request.jurisdiction or "",
            additional_instructions=request.additional_instructions or "",
        )

        generated_content = sanitize_text(
            generated_content
        )

        return DocumentResponse(
            success=True,
            document_type=request.document_type,
            content=generated_content,
            message="Document generated successfully."
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {str(error)}"
        )
