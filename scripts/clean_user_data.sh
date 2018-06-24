#!/bin/bash

echo 'Limpando os arquivos de usuário'

# Client cleanup
rm -r client/home

# Server cleanup
rm server/user_data.yaml
rm -r server/database
