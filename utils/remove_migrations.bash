#!/usr/bin/env bash
find .. -path "*/migrations/*.py" -not -name "__init__.py" -delete -print
find .. -path "*/migrations/*.pyc" -delete -print
