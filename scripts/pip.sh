#!/bin/bash

pip freeze | grep -v "^-e" | xargs pip uninstall -y
pip install -U pip
pip install -U setuptools wheel
pip install -U APScheduler chromadb fastapi fastapi-pagination llama-index openai python-multipart psycopg[binary] requests sqlalchemy sse-starlette streamlit uvicorn[standard]
pip freeze > requirements.txt
sed "/^pkg-resources==0.0.0$/d" requirements.txt > ../requirements.txt
rm requirements.txt
