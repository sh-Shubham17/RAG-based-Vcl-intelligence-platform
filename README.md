# RAG based intelligence platform  

##Setup

```bash

python3 -m venv.venv
source.venv/bin/activate
pip install -r requirements.txt

cp.env.example.env     # then edit .envand add your GEMINI_API_KEY
```

Get a free API key from [Google AI Studio] (https://aistudio.google.com/apikey).

## Run

```bash
uvicorn app.main:app --reload
```

App info: http://127.0.0.1:8000/ <br>
Interactive docs: http://127.0.0.1:8000/docs <br>
Health: http://127.0.0.1:8000/api/health <br>
Gemini check: http://127.0.0.1:8000/api/1lm/check <br>