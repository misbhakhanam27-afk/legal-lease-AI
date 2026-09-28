from google import genai
from google.genai import types

try:
    from ..config import GEMINI_API_KEY, GEMINI_MODEL, MAX_DOCUMENT_LENGTH
except ImportError:
    from config import GEMINI_API_KEY, GEMINI_MODEL, MAX_DOCUMENT_LENGTH


class GeminiDocumentGenerator:

    def __init__(self):
        self.client = None

    def _initialize_client(self):

        if self.client is not None:
            return

        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing. Check your .env file."
            )

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
        jurisdiction: str = "",
        additional_instructions: str = "",
    ) -> str:

        self._initialize_client()

        prompt = f"""
You are LegalEase, an AI-assisted legal document drafting system.

Create a professional legal document using ONLY the information provided.

Document Type:
{document_type}

Parties:
{parties}

Effective Date:
{effective_date}

Terms and Conditions:
{terms}

Jurisdiction:
{jurisdiction or "Not specified"}

Additional Instructions:
{additional_instructions or "None"}

Rules:
- Do not invent facts.
- Use placeholders when information is missing.
- Use clear headings and numbered clauses.
- Use professional legal language.
- Do not provide false legal citations.
- Do not claim that the document is guaranteed to be legally valid.
- End with a short notice recommending review by a qualified legal professional.

Return ONLY the document.
"""

        try:

            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=8000
                )
            )

            content = response.text

            if not content:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            content = content.strip()

            if len(content) > MAX_DOCUMENT_LENGTH:
                content = content[:MAX_DOCUMENT_LENGTH]

            return content

        except Exception as error:

            print("\n========== GEMINI ERROR ==========")
            print(str(error))
            print("==================================\n")

            raise RuntimeError(
                f"Gemini API error: {str(error)}"
            )