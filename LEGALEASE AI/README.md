# LegalEase

LegalEase is an AI-Powered Legal Document Generator.

## Architecture

Frontend:
- Streamlit

Backend:
- FastAPI

AI:
- Google Gemini

Document Export:
- TXT
- DOCX
- PDF

## Running the Backend

Open a terminal:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000