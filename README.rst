[![Maintainability](https://api.codeclimate.com/v1/badges/a0dd8a4560d9fa9615f5/maintainability)](https://codeclimate.com/github/VilllageBookBuilders/backend-vbb-portal/maintainability)

Village Portal Backend
=============================
Village Portal is an open-sourced 'facility-based mentoring management platform'. Village Book Builders accelerates learners globally through virtual mentoring, learning libraries, and community-directed educational solutions. Village Portal helps schedule hundreds of virtual mentors with mentees worldwide; this connection catalyzes further impact. Other features are in development. Village Portal's mission is to enable mentors to teach courageous learners and communities how to fish. By increasing literacy, research, and educational skills, we hope to enable innovation economies in villages globally. Village Portal is an essential step towards a better future. Are you interested in the cause? Reach out to us at hr@villagebookbuilders.org. Learn more @ www.villagebookbuilders.org.


Front-End of Village Portal @ https://github.com/VilllageBookBuilders/frontend-vbb-portal.git

To Help, questions, comments, concerns, Email US at @ support@villagebookbuilders.org. 
    Our DEV Taskboard: https://app.zenhub.com/workspaces/villagebookbuilders-5f662d2ba0525c27f3a90388/board. 
        Join our weekly meetings: https://meet.google.com/btm-gwyo-uwr on Saturday at 9AM 


The Backend code for Village Book Builders Portal

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT


Intial Setup
------------
The following steps should be completed in order to properly run the vbb-backend-portal on your local machine. 
Some steps may vary based on your operating system and some installation steps may be skipped if the required packages are already installed.
If you encounter issues in this process which can't be resolved with a 20 minute Google search and debug, please reach out via the back-end channel of the VBB Slack group or support@villagebookbuilders.org


(first time global installations)
    1) Install python3+ [https://realpython.com/installing-python/]

    2) Install pip [https://pip.pypa.io/en/stable/installing/]

    3) Install postgresql [https://www.postgresql.org/download/]
    
    4) Install redis [https://redis.io/download]

    5) Create a database in postgresql titled `vbb` in postgresql [https://www.freecodecamp.org/news/how-to-get-started-with-postgresql-9d3bc1dd1b11/]

(to run)

    6) Clone and cd into the backend-vbb-portal repository

    7) Run `virtualenv env`

    8) Run `source env/bin/activate` (path may differ depending on where /activate is installed)

    9) Run `pip install -r requirements/local.txt`

    10) Run `python manage.py runserver`
    
    11) Run python manage.py migrate

(to run windows)
    1) ``py -m pip install --user virtualenv`` 
    
    2) ``py -m venv env`` 
    
    3) ``env\Scripts\activate.bat`` or in powershell ``env\Scripts\activate.ps1``
    
    4) ``pip install -r requirements.txt``  
    
    5) ``python manage.py runserver`` 
    
    6) ``python manage.py migrate``

(To use your local database)
You will need to point the application to your local database.

1) Navigate to config/settings/base.py

2) Set ``DATABASES = {"default": env.db("DATABASE_URL", default="postgres://{USERNAME}:{PASSWORD}@localhost:{PORT}//vbb")}``

3) ``git update-index --skip-worktree base.py``

(Front-end run commands): 1. ``npm i`` 2. ``npm run build``

*Settings*

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html



**Basic Commands**
------------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy vbb_backend

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html



Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd vbb_backend
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.





Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at  https://sentry.io/signup/?code=cookiecutter  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.


Deployment
----------

The following details how to deploy this application.


Heroku
^^^^^^

See detailed `cookiecutter-django Heroku documentation`_.

.. _`cookiecutter-django Heroku documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html



Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html



