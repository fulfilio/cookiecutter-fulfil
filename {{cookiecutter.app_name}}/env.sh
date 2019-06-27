export FLASK_APP=manage.py
export FULFIL_APP_ID={{ cookiecutter.fulfil_app_id }}
export FULFIL_APP_SECRET={{ cookiecutter.fulfil_app_secret }}
export {{ cookiecutter.app_name|upper }}_SECRET_KEY={{ cookiecutter.secret_key }}
export ENCR_KEY={{ cookiecutter.encryption_key }}

export REDIS_URL=redis://localhost:6379/0
export DATABASE_URI=postgres://{{ cookiecutter.app_name }}:{{ cookiecutter.app_name }}@localhost:5432/{{ cookiecutter.app_name }}