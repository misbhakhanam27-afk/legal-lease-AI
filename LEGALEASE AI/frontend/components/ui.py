import streamlit as st


def show_header():

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:20px;
        ">
            <h1>⚖️ LegalEase</h1>
            <p>
                AI-Powered Legal Document Generator
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_disclaimer():

    st.warning(
        "⚠️ LegalEase generates AI-assisted draft documents. "
        "The output should be reviewed by a qualified legal "
        "professional before signing or use."
    )
