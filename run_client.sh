#!/bin/bash

echo "Iniciando o ambiente virtual Pipenv"
pipenv shell

echo "Realizando a chamada do servidor"
python3 client/src/client.py
