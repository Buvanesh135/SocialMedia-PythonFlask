pre-requirments Installtion Command: 

sudo apt-get install libffi-dev gcc build-essential libssl-dev libffi-dev python3-dev  libpq-dev


export FLASK_CONFIG=development
export FLASK_ENV=development
export FLASK_APP=app.py


from factory import db
from uuid import uuid4
from SocialMedia.BaseModel import Base
from SocialMedia.Models import Users



SELECT 
    pg_terminate_backend(pid) 
FROM 
    pg_stat_activity 
WHERE 
    pid <> pg_backend_pid()
    AND datname = 'solution_makers';   
    