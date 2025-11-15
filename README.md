### SETUP LOCALE
### configurazione del ambiente creazione del environment locale (una sorta di m2)
    - python -m venv venv   ### CREAZIONE VENV
### attivaione della roba di sopra
    - venv\Scripts\activate ### ATTIVAZIONE VENV
### configurazione del gestione del packeging manager pyton
    - pip install pip-tools
 ### preparazione delle dipendenze per generazione txt delle dipendenze del progetto in essere
    - pip-compile requirements.in
 ### descrizione delle dipendenze e derivazione delle singole librerie   
    - pip install -r requirements.txt
 ###   NON disattivare il progetto
    - deactivate ### DISATTIVAZIONE VENV

### RUN LOCALE
    1. ATTIVAZIONE VENV 
        - venv\Scripts\activate 
    2. AVVIO SERVER 
        - python -m fastapi dev --port 9082  

### UPDATE LIBRARY
    - pip compile --upgrade requirements.in
    - pip install -r requirements.txt

### ADD NEW LIBRARY
    - pip compile requirements.in
    - pip install -r requirements.txt

### SWAGGER
    SWAGGER-UI: http://host:port/docs
    OPENAPI JSON: http://host:port/openapi.json

### POSTMAN
    - importare il file postman/collection.json

### DOCKER
    - docker-compose up -d --build
    - docker-compose down

### ELASTICMQ
    - http://localhost:9325



