#!/bin/sh
set -e

if [ "$API_DEBUG" = "1" ]; then
  echo "API: Starting Debug Config"
  export PYTHONUNBUFFERED=1;
  pip install debugpy==1.6.3;
  python -m debugpy --listen 0.0.0.0:5678 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug;
else
  echo "API: Starting Production Setting";
  # nginx;
  # guicorn;
  uvicorn app.main:app --host 0.0.0.0 --port 8000;
fi