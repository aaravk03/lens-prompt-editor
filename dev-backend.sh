#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:api --reload
