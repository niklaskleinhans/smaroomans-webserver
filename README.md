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

## Run
```bash
FLASK_APP=app.py FLASK_DEBUG=1 flask run
``` 
