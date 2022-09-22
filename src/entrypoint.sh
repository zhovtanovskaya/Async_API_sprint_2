#!/bin/sh

# Запустить uvicorn  из директории, в которой находится этот скрипт.
SCRIPT_DIR=$(dirname `realpath $0`)   # Путь к этому скрипту.
cd $SCRIPT_DIR
uvicorn main:app --host 0.0.0.0 --port 8000
