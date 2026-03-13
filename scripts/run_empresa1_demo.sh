#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

venv/bin/python manage.py migrate
venv/bin/python manage.py bootstrap_empresa1
venv/bin/python manage.py runserver
