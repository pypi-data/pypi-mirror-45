# Mezzanine API

[![PyPI](https://img.shields.io/pypi/v/mezzanine-cartridge-api.svg)](https://pypi.org/project/mezzanine-cartridge-api/)
[![Travis CI](https://travis-ci.com/jackvz/mezzanine-cartridge-api.svg?branch=production)](https://travis-ci.com/jackvz/mezzanine-cartridge-api)
[![License](https://img.shields.io/github/license/jackvz/mezzanine-cartridge-api.svg)](https://github.com/jackvz/mezzanine-cartridge-api/blob/master/license)
[![Codecov](https://img.shields.io/codecov/c/github/jackvz/mezzanine-cartridge-api/production.svg?token=b618b46fd1fc46118196eb4b83c9c73b)](https://codecov.io/gh/jackvz/mezzanine-cartridge-api/branch/production)

A REST Web API for the [Mezzanine content management system](http://mezzanine.jupo.org/) with the [Cartridge](http://cartridge.jupo.org/index.html) e-commerce extension.

Oh, and this will work even if you're just running a blog or any other Mezzanine website without the Cartridge package.

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sTZBGpQ)

## Features

Web API methods for Mezzanine objects, including sites, users, groups, pages, blog posts and settings, and Cartridge objects, including products, categories, carts and orders.

[Swagger-UI](https://swagger.io/tools/swagger-ui/) as development tool and documentation.

Comes with [API key authentication/authorisation](https://pypi.org/project/djangorestframework-api-key/) configured, but can also be configured to work with Password-based and/or Authorisation code OAuth2 authentication/authorisation.

Additional features:
- User create and activate methods that include password hashing and sending a verification email
- User update and partial update methods that include password hashing
- Methods for checking a user password and a user token
- Password reset methods that include sending a verification email
- Methods for e-commerce customisation: Handlers for billing/shipping, tax, payment and order placement, to execute any customisation work done in the Mezzanine site installation.

## Screenshots

API docs

![API docs](https://raw.githubusercontent.com/jackvz/mezzanine-cartridge-api/master/screenshot-api-docs.png)

API keys

![API keys](https://raw.githubusercontent.com/jackvz/mezzanine-cartridge-api/master/screenshot-add-api-key.png)

## Installation

Install [Python](https://www.python.org/)

## New installation

Install Mezzanine and Cartridge:
```bash
pip install mezzanine
pip install cartridge
```

Create a new Mezzanine project with Cartridge, and set up a clean development database by running:
```bash
mezzanine-project -a cartridge [project-name]
cd [project_name]
python manage.py createdb --noinput --nodata
```

You may need to set ALLOWED_HOSTS, DATABASES and SHOP_CURRENCY_LOCALE in your project's settings.py file before creating the database.

    ALLOWED_HOSTS = ['*']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.dev',
        }
    }

    SHOP_CURRENCY_LOCALE = 'en_GB.UTF-8'

Start a Python [virtual environment](https://virtualenv.pypa.io/en/latest/), install the requirements and run the development server:
```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Then see the following section on adding to an existing installation.

## Adding to an existing installation

With Mezzanine and Cartridge installed, add the package to your project's requirements.txt file:

    mezzanine-cartridge-api

Add the following to installed apps and middleware in your project's settings.py file:

    INSTALLED_APPS = (
        ...
        'corsheaders',
        'rest_framework',
        'rest_framework_api_key',
        'drf_yasg',
        'mezzanine_cartridge_api',
        ...
    )

    # Use `MIDDLEWARE_CLASSES` prior to Django 1.10
    MIDDLEWARE = [
        ...
        'corsheaders.middleware.CorsMiddleware',
        ...
    ]

For OAuth2 authentication/authorisation, also add the following to installed apps in your project's settings.py file:

    INSTALLED_APPS = (
        ...
        'oauth2_provider',
        'rest_framework.authtoken',
        ...
    )

Add the following to your project's urls.py file:

    urlpatterns = [
        ...
        url(r'^api/', include('mezzanine_cartridge_api.urls')),
        ...
    ]

Start the Python virtual environment, install the requirements and run the development server:
```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

## Configuration

The following configuration settings are available:

CORS_ORIGIN_ALLOW_ALL

And other [django-cors-middleware](https://pypi.org/project/django-cors-middleware/) settings.

REST_FRAMEWORK

See the [Django REST framework settings](https://www.django-rest-framework.org/api-guide/settings/).

SWAGGER_SETTINGS

See the [drf-yasg Swagger settings](https://drf-yasg.readthedocs.io/en/stable/settings.html#swagger-settings).

SWAGGER_SCHEME_HTTPS

True or False: Defaults to False. True for when your API is available over HTTPS.

## Notes

If you are using the included Swagger UI to test your API and get a message "CSRF Failed: CSRF token missing or incorrect", be sure to log out of the Mezzanine site.

If you are using the included Swagger UI to test your API and get a message "TypeError: Failed to fetch", and you are running a secure site (over HTTPS), be sure to select the HTTPS scheme from the Shemes dropdown. This dropdown keeps reverting to HTTP in the Swagger UI, so you may have to select it again after making API call changes and/or selecting API methods.
