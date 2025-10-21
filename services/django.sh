#!/bin/bash

uv run openbox/artifact/manage.py migrate && uv run openbox/artifact/manage.py runserver 0.0.0.0:8000
