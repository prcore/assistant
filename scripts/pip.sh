#!/bin/bash

pip freeze | grep -v "^-e" | xargs pip uninstall -y
pip install -U pip
pip install -U setuptools wheel
pip install -U APScheduler bs4 chromadb fastapi fastapi-pagination langchain openai python-multipart psycopg[binary] requests sqlalchemy sse-starlette streamlit tiktoken uvicorn[standard]
pip freeze > requirements.txt
sed "/^pkg-resources==0.0.0$/d" requirements.txt > ../requirements.txt
rm requirements.txt
