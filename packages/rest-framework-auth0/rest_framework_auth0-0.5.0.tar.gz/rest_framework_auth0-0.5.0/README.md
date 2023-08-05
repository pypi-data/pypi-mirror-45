=====
djangorestframework-auth0
=====

Migrate from 0.2.1 to >0.4.5
---
**If you're using the version 0.2.1 -or older- from this package, you'll need to update your Auth0 settings**

From this
``` python
AUTH0 = {
    'AUTH0_CLIENT_ID': '<YOUR_AUTH0_CLIENT_ID>', # make sure it's the same string that aud attribute in your payload provides
    'AUTH0_CLIENT_SECRET': '<YOUR_AUTH0_CLIENT_SECRET>',
    'CLIENT_SECRET_BASE64_ENCODED': True,  # default to True, if you're Auth0 user since December, maybe you should set it to False
    ...
}

```

To this
``` python
AUTH0 = {
  'CLIENTS': {
      'default': {
          'AUTH0_CLIENT_ID': '<YOUR_AUTH0_CLIENT_ID>',  #make sure it's the same string that aud attribute in your payload provides
          'AUTH0_CLIENT_SECRET': '<YOUR_AUTH0_CLIENT_SECRET>',
          'CLIENT_SECRET_BASE64_ENCODED': True,  # default to True, if you're Auth0 user since December, maybe you should set it to False,
          'AUTH0_ALGORITHM': 'HS256',  # HS256 or RS256
          'PUBLIC_KEY': <YOUR_AUTH0_CERTIFICATE>,  # used only for RS256
      }
  },
  ...
}
```

***If you wanna use RS256, please follow the [sample project][sample]***


___

Library to simply use Auth0 token authentication in DRF within djangorestframework-jwt

This library let you to login an specific user based on the JWT Token returned by Auth0 Javascript libraries


Detailed documentation will be in the "docs" directory.

Installation
-----------

1. Using `pip` install the library cloning the repository with following command:
``` shell
pip install rest_framework_auth0
```

Quick start
-----------

1. Add "django.contrib.auth to INSTALLED_APPS settings like this:
``` python
INSTALLED_APPS = [
    ...
    'django.contrib.auth',
    ...
]
```
This will allow us to login as an specific user as well as auto-creating users when they don't exist

1. Add "rest_framework_auth0" to your INSTALLED_APPS **after** `rest_framework_jwt` setting like this:
``` python
INSTALLED_APPS = [
    ...,
    'rest_framework_jwt',
    'rest_framework_auth0',
]
```

2. Add `Auth0JSONWebTokenAuthentication` in your DEFAULT_AUTHENTICATION_CLASSES located at settings.py from your project:
``` python
REST_FRAMEWORK = {
    ...,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...,
        'rest_framework_auth0.authentication.Auth0JSONWebTokenAuthentication',
    ),
}
```

3. Add your AUTH0_CLIENT_SECRET and AUTH0_CLIENT_ID in your settings.py file -must be the same secret and id than the frontend App-:
``` python
AUTH0 = {
  'CLIENTS': {
      'default': {
          'AUTH0_CLIENT_ID': '<YOUR_AUTH0_CLIENT_ID>',  #make sure it's the same string that aud attribute in your payload provides
          'AUTH0_CLIENT_SECRET': '<YOUR_AUTH0_CLIENT_SECRET>',
          'CLIENT_SECRET_BASE64_ENCODED': True,  # default to True, if you're Auth0 user since December, maybe you should set it to False
      }
  },
  'AUTH0_ALGORITHM': 'HS256',  # default used in Auth0 apps
  'JWT_AUTH_HEADER_PREFIX': 'JWT',  # default prefix used by djangorestframework_jwt
  'AUTHORIZATION_EXTENSION': False,  # default to False
  'USERNAME_FIELD': 'sub',  # default username field in auth0 token scope to use as token user
}
```

4. Add the `Authorization` Header to all of your REST API request, prefixing JWT to your token:
```
Authorization: JWT <AUTH0_GIVEN_TOKEN>
```
5. Use the decorator `@token_required` in all views you want to protect (not_ready_yet)

6. That's it

Multiple Clients - Multiples App - One API
-----------
If you wanna to use multiple Auth0 App and/or Clients -for example if you're creating an open API, you can add as much as you want in the **AUTH0.CLIENTS** settings parameter

``` python
AUTH0 = {
  'CLIENTS': {
      'default': {
          'AUTH0_CLIENT_ID': '<YOUR_AUTH0_CLIENT_ID>',  #make sure it's the same string that aud attribute in your payload provides
          'AUTH0_CLIENT_SECRET': '<YOUR_AUTH0_CLIENT_SECRET>',
          'CLIENT_SECRET_BASE64_ENCODED': True,  # default to True, if you're Auth0 user since December, maybe you should set it to False
      }
      'web': {
          'AUTH0_CLIENT_ID': '<YOUR_AUTH0_CLIENT_ID>',  #make sure it's the same string that aud attribute in your payload provides
          'AUTH0_CLIENT_SECRET': '<YOUR_AUTH0_CLIENT_SECRET>',
          'CLIENT_SECRET_BASE64_ENCODED': True,  # default to True, if you're Auth0 user since December, maybe you should set it to False
      }
      'mobile': {
          'AUTH0_CLIENT_ID': '<YOUR_AUTH0_CLIENT_ID>',  #make sure it's the same string that aud attribute in your payload provides
          'AUTH0_CLIENT_SECRET': '<YOUR_AUTH0_CLIENT_SECRET>',
          'CLIENT_SECRET_BASE64_ENCODED': True,  # default to True, if you're Auth0 user since December, maybe you should set it to False
      }
  },
  ...
}
```

In order to select one of them when the authentication is needed -a POST request, for example- you need to add a header called **Client-Code** -by default, but you can customize it-.
The names of the clients are **case sensitive**.

Sample project
-----------

A sample project can be found [here][sample]

[sample]: https://github.com/mcueto/djangorestframework-auth0_sample
