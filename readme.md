# When you want to resume on a fresh machine:

### 1. Clone the repo

- git clone https://github.com/hritickjaiswal22/ai-agents.git
- cd agno-agents

### 2. Recreate virtual environment

- uv venv --python 3.12
- source .venv/bin/activate

### 3. Reinstall dependencies

- uv pip install -r requirements.txt

### 4. Set your API key

- export ANTHROPIC_API_KEY=sk-...

### 5. Run

- fastapi dev web_search_agent.py

### 6. Open os.agno.com and sign in.
