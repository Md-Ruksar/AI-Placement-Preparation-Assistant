# AI Placement Preparation Assistant

AI Placement Preparation Assistant is a web application built with Python and Streamlit that helps students prepare for campus placements. It provides practice quizzes, interview simulation, resume and skill-gap tools, and an AI career assistant powered by Google Gemini with a Hugging Face fallback.

## Features

- **Dashboard** — track questions attempted, overall score and progress across all modules
- **Aptitude Practice** — quantitative, logical reasoning and verbal ability questions
- **Technical Interview** — Python, OOP and DBMS questions with explanations
- **HR Interview** — common HR interview questions with model answers
- **Mock Interview** — mixed interview simulation with performance accuracy
- **Resume Analysis** — upload a resume and extract text and word count
- **Skill Gap Analysis** — per-module performance report and recommended focus areas
- **AI Career Assistant** — chat about placement preparation, interviews and careers
- **Gemini AI with Hugging Face fallback** — if Gemini is unavailable, the assistant automatically falls back to the Hugging Face API, then to a friendly error message

## Tech Stack

- Python 3.11.9
- Streamlit
- Google GenAI (Gemini)
- Requests
- Python-Dotenv
- Hugging Face Inference API (fallback)

## Installation

```text
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux, activate with `source venv/bin/activate` instead.

## Environment Variables

Create a `.env` file in the project root (it is gitignored — never commit it):

```text
GEMINI_API_KEY=your_key_here
HF_TOKEN=your_token_here
```

## Run

```text
streamlit run app.py
```

## Deployment — Streamlit Community Cloud

1. Push this project to a GitHub repository containing only: `app.py`, `requirements.txt`, `README.md`, `.gitignore`.
   Do **not** commit `.env` or `venv/`.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app** → select the repository, branch and `app.py`.
3. Open **Advanced settings → Secrets** and add:

```text
GEMINI_API_KEY = "your_key_here"
HF_TOKEN = "your_token_here"
```

4. Deploy. Streamlit Cloud installs only the packages listed in `requirements.txt`.

Note: `.env` is not uploaded to the cloud, so the API keys must be added in the Streamlit Cloud secrets settings.