import os

import streamlit as st

try:
    from .components.ui import (
        show_header,
        show_disclaimer,
    )
    from .utils.api_client import generate_document
    from .utils.preview import format_html_preview
    from .utils.exporters import (
        format_txt,
        format_docx,
        format_pdf,
    )
except ImportError:  # pragma: no cover
    from components.ui import (
        show_header,
        show_disclaimer,
    )
    from utils.api_client import generate_document
    from utils.preview import format_html_preview
    from utils.exporters import (
        format_txt,
        format_docx,
        format_pdf,
    )


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)


# --------------------------------------------------
# BACKEND URL
# --------------------------------------------------

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
    }

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 45px;
        font-size: 16px;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

show_header()

show_disclaimer()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    st.write(
        "Backend:"
    )

    st.code(
        BACKEND_URL
    )

    st.info(
        "Make sure the FastAPI backend is "
        "running before generating a document."
    )


# --------------------------------------------------
# DOCUMENT INPUTS
# --------------------------------------------------

st.subheader(
    "📄 Create Your Legal Document"
)


document_type = st.selectbox(
    "Document Type",
    [
        "Employment Contract",
        "Lease Agreement",
        "Non-Disclosure Agreement (NDA)",
        "Service Agreement",
        "Partnership Agreement",
        "Internship Agreement",
        "Freelance Agreement",
        "General Legal Agreement",
    ]
)


parties = st.text_area(
    "👥 Parties",
    placeholder=(
        "Example:\n"
        "Employer: ABC Technologies Pvt. Ltd.\n"
        "Employee: John Smith"
    ),
    height=130,
)


terms = st.text_area(
    "📋 Terms and Conditions",
    placeholder=(
        "Example:\n"
        "Salary: ₹30,000 per month;\n"
        "Working hours: 9 AM to 6 PM;\n"
        "Leave: 15 days per year;\n"
        "Notice period: 30 days"
    ),
    height=180,
)


effective_date = st.text_input(
    "📅 Effective Date",
    placeholder="Example: 1 October 2026"
)


jurisdiction = st.text_input(
    "⚖️ Jurisdiction",
    placeholder="Example: Chennai, Tamil Nadu, India"
)


additional_instructions = st.text_area(
    "➕ Additional Instructions",
    placeholder=(
        "Optional instructions for the AI..."
    ),
    height=100,
)


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

st.divider()

generate_button = st.button(
    "✨ Generate Legal Document"
)


if generate_button:

    if not parties.strip():

        st.error(
            "Please enter the party details."
        )

        st.stop()

    if not terms.strip():

        st.error(
            "Please enter the terms and conditions."
        )

        st.stop()

    if not effective_date.strip():

        st.error(
            "Please enter the effective date."
        )

        st.stop()

    with st.spinner(
        "Generating your legal document..."
    ):

        try:

            result = generate_document(
                backend_url=BACKEND_URL,
                document_type=document_type,
                parties=parties,
                terms=terms,
                effective_date=effective_date,
                jurisdiction=jurisdiction,
                additional_instructions=additional_instructions,
            )

            st.session_state[
                "generated_document"
            ] = result["content"]

            st.session_state[
                "generated_type"
            ] = document_type

            st.success(
                "✅ Document generated successfully!"
            )

        except Exception as error:

            st.error(
                f"❌ Could not generate document.\n\n"
                f"{error}"
            )


# --------------------------------------------------
# DISPLAY GENERATED DOCUMENT
# --------------------------------------------------

if "generated_document" in st.session_state:

    st.divider()

    st.subheader(
        "📝 Generated Document"
    )

    edited_document = st.text_area(
        "Edit your document if required:",
        value=st.session_state[
            "generated_document"
        ],
        height=600,
    )

    # Keep edited version
    st.session_state[
        "generated_document"
    ] = edited_document


    # --------------------------------------------------
    # PREVIEW
    # --------------------------------------------------

    st.subheader(
        "👁️ Document Preview"
    )

    preview_html = format_html_preview(
        edited_document
    )

    st.markdown(
        f"""
        <div style="
            border:1px solid #ddd;
            border-radius:10px;
            padding:25px;
            background-color:white;
        ">
            {preview_html}
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # DOWNLOAD SECTION
    # --------------------------------------------------

    st.subheader(
        "⬇️ Download Document"
    )

    col1, col2, col3 = st.columns(3)


    with col1:

        txt_file = format_txt(
            edited_document
        )

        st.download_button(
            label="📄 Download TXT",
            data=txt_file,
            file_name="legalease_document.txt",
            mime="text/plain",
        )


    with col2:

        docx_file = format_docx(
            edited_document,
            st.session_state[
                "generated_type"
            ]
        )

        st.download_button(
            label="📝 Download DOCX",
            data=docx_file,
            file_name="legalease_document.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument"
                ".wordprocessingml.document"
            ),
        )


    with col3:

        pdf_file = format_pdf(
            edited_document,
            st.session_state[
                "generated_type"
            ]
        )

        st.download_button(
            label="📕 Download PDF",
            data=pdf_file,
            file_name="legalease_document.pdf",
            mime="application/pdf",
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "LegalEase | AI-Powered Legal Document Generator"
)