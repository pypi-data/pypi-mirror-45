=======
Proplan
=======

Django application to assign a tasks, defining bugs and planning of your
project.


Installation
------------

.. code-block:: shell

    pip3 install django-proplan


Quick start
-----------

1. Add "proplan" to your INSTALLED_APPS setting like this:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'proplan',
    ]

2. Include the polls URLconf in your project urls.py like this:

.. code-block:: python

    path('plan/', include('proplan.urls')),

3. Run `python3 manage.py migrate` to create the Proplan models.

4. Run `python3 manage.py createsuperuser` to create the user if you don't
   have one.

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to login (you'll need the Admin app enabled).

6. Visit http://127.0.0.1:8000/plan/ to create your plan of work on project.


Automatic Bug System
--------------------

The Proplan allows you to enable automatic publication of errors that have
occurred in the project through ABS - Automatic Bug System. There are 2
ways to do this:

1. Logging errors directly to server.
2. Sending errors through API.


Logging errors
~~~~~~~~~~~~~~

Connect "proplan.log.ABSHandler" to your LOGGING setting like this:

.. code-block:: python

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        ...
        'handlers': {
            ...
            'abs': {
                'class': 'proplan.log.ABSHandler',
                'level': 'ERROR',
            }
        },
        'loggers': {
            ...
            'django': {
                'handlers': ['abs'],
                'level': 'ERROR',
            },
        },
    }


Sending errors
~~~~~~~~~~~~~~

1. Add "ABS_KEY" to your PROPLAN setting like this:

.. code-block:: python

    PROPLAN = {
        ...
        'ABS_KEY': 'cookie-supported-key',
    }

2. Make POST response with data of bug to API:

.. code-block:: shell

    curl -H 'Cookie: proplanabs=cookie-supported-key' \
    --data-urlencode 'title=Bug in mobile app&message=More...' \
    http://127.0.0.1:8000/plan/abs/create/


Settings
--------

All next settings must be within the dictionary `PROPLAN`, when you
define them in the file settings.py

ACCESS_FUNCTION
~~~~~~~~~~~~~~~

Function that checks access to resources. You may want to use:

1. `proplan.access.authenticated` - for authenticated users.
2. `proplan.access.staff` - for employers and superusers.
3. `proplan.access.superuser` - for superusers only.
4. `proplan.access.view_thread` - for users with view permission for Thread
   model.
5. any custom function.

The default is the internal function `proplan.access.view_thread`.

ABS_KEY
~~~~~~~

The options for Automatic Bug System. While there is no key, the system does
not work. By default no key.

ABS_COOKIE_NAME
~~~~~~~~~~~~~~~

The cookie name for checking the ABS key. By default is `proplanabs`.

ATTACH_UPLOAD_PATH
~~~~~~~~~~~~~~~~~~

Path to uploading files. By default is:

.. code-block:: python

    'proplan/attaches/%(date)s/%(code)s/%(filename)s'

ATTACH_THUMB_SIZE
~~~~~~~~~~~~~~~~~

The size of the thumbnails for attached images. By default is:

.. code-block:: python

    (300, 300)

ATTACH_THUMB_EXTENSIONS
~~~~~~~~~~~~~~~~~~~~~~~

List of recognized image extensions to be previewed. By default is:

.. code-block:: python

    ['.png', '.jpg', '.jpeg', '.bmp']


PRIORITIES
~~~~~~~~~~

List of recognized image extensions to be previewed. By default is:

.. code-block:: python

    [
        (1, _('low')),
        (2, _('normal')),
        (3, _('high')),
        (4, _('urgent')),
        (5, _('immediate')),
    ]
