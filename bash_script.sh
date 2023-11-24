#!/usr/bin/env bash
# Script to execute when deploying on render.com
/opt/render/project/src/.venv/bin/python -m pip install --upgrade pip
pip install Flask
pip install sqlalchemy
pip install gunicorn
gunicorn --version
pip install flask_sqlalchemy
