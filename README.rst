cookiecutter-fulfil
==================

A Fulfil Flask template for cookiecutter_.

.. _cookiecutter: https://github.com/audreyr/cookiecutter


You can use this to get a ready to use boilerplate to build a
Flask App that connects to Fulfil.


When to use the template
------------------------

* You need Fulfil Authentication to access the app
* You need a SQL backend (sqlalchemy is included)

Use it now
----------
::

    $ pip install cookiecutter
    $ cookiecutter git@github.com:fulfilio/cookiecutter-fulfil.git

You will be asked about your basic info (name, project name, app name, etc.).
This info will be used in your new project.

A folder with the app name will be created for you.

The script also creates a convenient env.sh file with all the environment
variables. This is gitignored so you don't accidentally check the file in
to source control.

To set the environment variables use::

   cd project-folder/
   source env.sh
