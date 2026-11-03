# New Gen AI 2.4

A Streamlit-based collection of AI-assisted learning and research tools. This repository contains the Python modules from the supplied `New_GEN_AI_2_4.zip`; bundled databases, bytecode caches, and nested archive copies were left out.

## Requirements

- Python 3.10 or 3.11 recommended
- An OpenAI API key for features that call OpenAI

## Setup (Windows PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and set your own OPENAI_API_KEY value
streamlit run assesment5.py
```

The `.env` file is ignored by Git. Never commit API keys. Alternatively, copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`, enter your own key, and keep that file local.

## Project layout

The main multi-tool interface is `assesment5.py`; the other Python files provide feature modules and standalone tools. `papersetter.py`, `academic_integrity_checking.py`, `data_analysis_tools.py`, `research_methodology_guidance.py`, and `syllabus_optimization.py` also contain individual Streamlit interfaces.

## Before publishing

Review code and dependencies, and confirm you have permission to publish all content. Add only data you are authorized to share. No personal databases or user uploads are included here.
