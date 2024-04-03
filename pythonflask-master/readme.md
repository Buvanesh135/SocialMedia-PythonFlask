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
    

    {"web":{"client_id":"164192920835-abp15k3pgjsouogrd4dv0rilttojok25.apps.googleusercontent.com","project_id":"my-project-401704","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost/callback"]}}