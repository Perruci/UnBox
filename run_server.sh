#!/bin/bash

bash init_environment.sh

echo "Realizando a chamada do servidor"
python3 server/src/main.py
