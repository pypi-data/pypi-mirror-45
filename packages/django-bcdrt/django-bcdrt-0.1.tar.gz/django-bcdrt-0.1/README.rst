=====
BriteCore Dynamic Risk Types
=====

This app was built in response to a test requirement
Quick start
-----------

1. Add "main" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'bcdrt',
    ]

2. Include the main URLconf in your project urls.py like this::

    path('', include('bcdrt.urls')),

3. Run `python manage.py migrate` to create the risk models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a risk (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/ to subscribe to a risk type.
5. Visit http://127.0.0.1:8000/risks/ to get a specific risktype in Json
5. Visit http://127.0.0.1:8000/risks/<risktype> to get a specific risktype in Json