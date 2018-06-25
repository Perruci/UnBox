UnBox: Aplicação Dropbox-like TCP/IP 
====================================

### Trabalho final da disciplina Transmissão de Dados 2018.1 da Universidade de Brasília (UnB-CIC)
Autoria
-------
* **Autor: Pedro Henrique Suruagy Perruci | pedro.perruci@gmail.com | 14/0158596**
* Professor: Marcos F. Caetano | mfcaetano@unb.br
* Monitoras:
  * Camila Camargo | 130104868@aluno.unb.br
  * Mariana Makiuchi | marimakiuchi@aluno.unb.br
  
Objetivos
----------
Através do desenvolvimento do sistema UnBox pretende-se aplicar os conhecimentos explorados na disciplina Transmissão de Dados.
Os principais conceitos trabalhados são a implementação de um sistema na camada de aplicação do modelo OSI e o desenvolvimento de um protocolo de comunicação simplificado cliente-servidor capaz de realizar as operações especificadas.
Os conceitos chaves da aplicação são a **sincronização** e o **armazenamento** de arquivos do usuário.

Ao lidar com a manipulação de arquivos e o acesso concorrente ao servidor também é possivel relembrar, ou adiantar, conceitos das disciplinas de Organização de Arquivos e Processamento em Tempo Real, embora não sejam o foco deste trabalho.

Especificações
---------------
Tendo como referência as especificações propostas no roteiro do trabalho, estipulou-se os seguintes requisitos para o sistema:

1. Aplicação em linha de comando compatível com sisetmas linux;
2. Cliente e servidor se comunicam em rede e operam em pastas diferentes;
3. O servidor é capaz de atender múltiplos clientes simultâneamente;
4. Sincronização entre arquivos no cliente e servidor de forma persistente;
5. Operações realizadas tanto no cliente, como no servidor são armazenadas em arquivos log.

Estas especificações serão abordadas individualmente nas seções seguintes.

### Linguagem e Dependências
O sistema foi desenvolvido na linguagem Python 3.6.5, em ambiente OSX 10.13.5. 
O funcionamento do sistema em sistema Ubuntu 16.04 foi verificado como adequado.

Todas as dependências foram armazenadas em um ambiente virtual [Pipenv](https://docs.pipenv.org).
Portanto para a execução da aplicação é necessária apenas a instalação do ambiente virtual.
```bash
sudo apt-get install -y python3-pip
pip3 install pipenv
```

Uma lista completa dos módulos utilizadas no sistema está expressa a seguir:
* Python 3.6.5
    * ruamel.yaml (pipenv)
    * socket
    * threading
    * logging
    * time
    * sys
    * os
    
### Disposição de Arquivos
A disposição de arquivos esperada ao executar-se o sistema está disposta a seguir.
Os arquivos destacados são criados durante a execução da aplicação e desempenham função essencial no sistema.
Note que a pasta 'UnBox/scripts' contém alguns arquivos executáveis úteis para a utilização e manutenção da aplicação
```
UnBox
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── client
│   ├── client_history.log     <- Client Log
│   ├── home
│   │   └── [Client Workspace] <- Client Workspace
│   └── src
│       ├── main.py
│       ├── main_window.py
│       ├── network_client.py
│       └── unbox_client.py
├── scripts
│   ├── clean_logs.sh
│   ├── clean_user_data.sh
│   ├── init_environment.sh
│   ├── run_client.sh
│   └── run_server.sh
└── server
    ├── database                <- Server Database
    │   └── [Server Files]
    ├── server_history.log      <- Server Log
    ├── src
    │   ├── client_thread.py
    │   ├── database.py
    │   ├── main.py
    │   ├── server_network.py
    │   └── unbox_server.py
    └── user_data.yaml          <- Persistent User Information
```

### Instruções de Execução
Para a chamada adequada do sistema UnBox recomenda-se acessar o diretório root do projeto e inicializar o ambiênte virtual.
Este procedimento deve ser realizado em cada terminal utilizado. 
```bash
cd path/to/UnBox
bash scripts/init_environment.sh
```
Em seguida, realiza-se a chamada do programa server-side pela chamada do script run_server.sh
```bash
cd path/to/UnBox # caso tenha mudado o diretório
bash scripts/run_server.sh
```
Para realizar a chamada do aplicação client-side pela seguinte chamada.
```bash
cd path/to/UnBox # caso tenha mudado o diretório
bash scripts/run_server.sh
```
**Importante:** A chamada dos scripts de execução do cliente e do servidor devem ser feitas do diretorio UnBox/.
Os caminhos relativos de arquivos importantes parte deste diretório.
