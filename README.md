### SETUP INIZIALE

## ELASTIMQ
    Contenitore delle code SQS in locale, per visualizzare la console web:
    - Copiare la cartella elasticmq nella cartella di destinazione
    - Eseguire il comando docker-compose up -d nella cartella di destinazione
    - Verifica http://localhost:9325

## COMPILAZIONE AMBIENTE DI SVILUPPO LOCALE
    1. Creazione VENV
    - python -m venv venv   

    2. Attivazione VENV
    - venv\Scripts\activate ### ATTIVAZIONE VENV

    3. Configurazione del gestione del packging manager pyton
    - pip install pip-tools
    
    4. Installazione delle dipendenze 
    - pip install -r requirements.txt
    - docker compose -f .\docker-compose-compile-requirements.yml run --rm compiler

### RUN LOCALE
    1. Assicurarsi di aver attivato il VENV 
        - venv\Scripts\activate 
    2. Avvio server fastapi
        - cd src
        - python -m fastapi dev --port xxxx 

### DOCKER
    CREAZIONE E AVVIO AMBIENTE DOCKER CONTAINER
    - docker-compose up -d --build
    - docker-compose down

### SWAGGER
    http://host:port/docs

### OPENAPI JSON
    http://host:port/openapi.json

### ALEMBIC
    - alembic revision --autogenerate -m "YYYYMMDDHH_NAU_XXX"
    - alembic [-x tenant=<tenant_name>] upgrade head
    - alembic [-x tenant=<tenant_name>] downgrade -1
    - alembic current
    - alembic history
    - alembic heads
    - alembic branches
    - alembic show <revision>


