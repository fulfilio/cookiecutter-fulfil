export FLASK_APP=autoapp.py
export FULFIL_APP_ID={{ cookiecutter.fulfil_app_id }}
export FULFIL_APP_SECRET={{ cookiecutter.fulfil_app_secret }}
export {{ cookiecutter.app_name|upper }}_SECRET_KEY={{ cookiecutter.secret_key }}
export ENCR_KEY={{ cookiecutter.encryption_key }}
