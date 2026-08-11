# ScholarFlow AI

ScholarFlow AI is a single-server research-paper formatting application.

The React/Vite frontend extracts text from an uploaded PDF. The Flask API sends
that extracted manuscript through the formatting pipeline:

1. CrewAI academic formatting
2. Markdown manuscript generation
3. LaTeX generation
4. PDF compilation

## Project layout

```text
research-paper-ai/
├── frontend/                  React/Vite source
├── frontend_dist/             production frontend served by Flask
├── src/research_paper_ai/
│   ├── api/                   Flask API
│   ├── pipeline/              formatting pipeline
│   ├── services/              formatter/LaTeX/PDF services
│   ├── llm/                   LLM adapters
│   └── models/                data models
├── workspace/
│   └── output/                generated files
├── requirements.txt
├── pyproject.toml
└── run.sh
```

## Requirements

- Python 3.11, 3.12, or 3.13
- Node.js 18+
- npm
- A working LaTeX installation with `pdflatex`
- A CrewAI-supported LLM provider

The current formatter uses Groq through `GROQ_API_KEY`.

## Setup

```bash
cd research-paper-ai

python3.11 -m venv venv
source venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

cp .env.example .env
```

Set the required environment variable in `.env`:

```text
GROQ_API_KEY=your_key_here
```

Optional model override:

```text
GROQ_MODEL=groq/llama-3.3-70b-versatile
```

Do not commit `.env` or expose API keys.

## Run

```bash
./run.sh
```

Open:

```text
http://localhost:5002
```

The script builds the React application into `frontend_dist/` and then starts
Flask on port `5002`.

## API

### Health

```bash
curl http://localhost:5002/health
```

### Format a manuscript

```bash
curl -X POST http://localhost:5002/format-paper   -H "Content-Type: application/json"   -d '{"paper_content":"# Title\n\nMy paper..."}'
```

A successful response contains URLs for:

- generated PDF
- generated LaTeX
- generated Markdown manuscript
- generated BibTeX

## Frontend development

Terminal 1:

```bash
PYTHONPATH=src python src/research_paper_ai/api/app.py
```

Terminal 2:

```bash
cd frontend
npm install
npm run dev
```

The Vite development server proxies `/format-paper`, `/download/*`, and
`/health` to Flask on port `5002`.

## Notes

The repository contains older research-pipeline experiments and tests from
earlier iterations. The supported production path in this project is the
ScholarFlow formatter under `pipeline/formatter_pipeline.py`.
