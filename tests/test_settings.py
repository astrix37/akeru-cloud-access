import os

POLICY_BUCKET = "abc-def"
POLICY_PREFIX = "ghi"
DEFAULT_TRUSTED_USERS = ["jkl"]
SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "akeru"
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        'NAME': os.path.join('db.sqlite3'),
    }
}
