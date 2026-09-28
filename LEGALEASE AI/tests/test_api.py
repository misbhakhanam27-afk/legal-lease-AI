def test_project_structure():

    import os

    assert os.path.exists("frontend")
    assert os.path.exists("backend")


def test_backend_app_imports_from_project_root():

    import backend.main

    assert backend.main.app.title == "LegalEase"


def test_default_gemini_model_is_supported():

    import backend.config as config

    assert config.GEMINI_MODEL == "gemini-3.8-flash"