import requests


def generate_document(
    backend_url: str,
    document_type: str,
    parties: str,
    terms: str,
    effective_date: str,
    jurisdiction: str,
    additional_instructions: str,
):

    url = f"{backend_url.rstrip('/')}/generate"

    payload = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "effective_date": effective_date,
        "jurisdiction": jurisdiction,
        "additional_instructions": additional_instructions,
    }

    response = requests.post(
        url,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    return response.json()
