from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()
text = 'SECRET_KEY = \'{0}\''.format(secret_key)

with open("config/local_setting.py", "w") as f:
    print(text, file=f)


