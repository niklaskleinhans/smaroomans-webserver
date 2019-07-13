# Smaroomans webserver
## Installation
Create Virtualenv
```bash 
virtualenv --python `which python3` venv
source venv/bin/activate
```

Install Dependencies
```bash
pip install -r requirements.txt
```

Setup Mongo DB
- Download :  https://www.mongodb.com/download-center/community
- start mongo db as a service

insert database
```bash
mongodb  
use smaroomansDatabase
exit
```


## Run
```bash
FLASK_APP=app.py FLASK_DEBUG=0 flask run
``` 
