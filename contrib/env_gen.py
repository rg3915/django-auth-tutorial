"""
Python SECRET_KEY generator.
"""
import random

chars = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
size = 50
secret_key = "".join(random.sample(chars, size))

chars = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%_"
size = 20
password = "".join(random.sample(chars, size))

CONFIG_STRING = """
DEBUG=True
SECRET_KEY=%s
ALLOWED_HOSTS=127.0.0.1, .localhost

#DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
#DB_NAME=
#DB_USER=
#DB_PASSWORD=%s
#DB_HOST=localhost

#EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DEFAULT_FROM_EMAIL=noreply@admin.com
EMAIL_HOST=0.0.0.0
EMAIL_PORT=1025
EMAIL_HOST_USER=noreply@admin.com
EMAIL_HOST_PASSWORD=p4ssw0rd
EMAIL_USE_TLS=False
""".strip() % (secret_key, password)

# Writing our configuration file to '.env'
with open('.env', 'w') as configfile:
    configfile.write(CONFIG_STRING)

print('Success!')
print('Type: cat .env')
