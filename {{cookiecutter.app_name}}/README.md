<a href="https://fulfil.io/">
    <img src="https://cdn.fulfil.io/assets/logo/full-transparent.png" alt="Fulfil.IO" title="Fulfil.IO" align="right" height="60" />
</a>

# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Table of content

- [Quickstart](#quickstart)
- [Shell](#shell)
- [Running Tests](#running-tests)
- [Migrations](#migrations)
- [Documentation](#documentation)

## Quickstart

First, set your app's secret key as an environment variable. For example,
add the following to ``.bashrc`` or ``.bash_profile``.

```sh
    export {{ cookiecutter.app_name|upper }}_SECRET='something-really-secret'
    export FULFIL_APP_ID=app-id
    export FULFIL_APP_SECRET=api-secret
```

Run the following commands to bootstrap your environment:

```sh
    git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.app_name }}
    cd {{ cookiecutter.app_name }}
    pip install -r requirements.txt
```

You will see a pretty welcome screen.

In general, before running shell commands, set the ``FLASK_APP`` and
``FLASK_DEBUG`` environment variables:

```sh
    export FLASK_APP=/path/to/autoapp.py
    export FLASK_DEBUG=1
```

Once you have installed your DBMS, run the following to create your app's
database tables and perform the initial migration:

```sh
    flask db init
    flask db migrate
    flask db upgrade
    flask run
```

## Shell


To open the interactive shell, run:

```sh
    flask shell
```

By default, you will have access to the flask ``app``.


## Running Tests

To run all tests, run:
```sh
    flask test
```


## Migrations

Whenever a database migration needs to be made. Run the following commands:

```sh
    flask db migrate
```

This will generate a new migration script. Then run:

```sh
    flask db upgrade
```

To apply the migration.

For a full migration command reference, run ``flask db --help``.
