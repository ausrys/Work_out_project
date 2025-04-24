import environ
env = environ.Env()
environ.Env.read_env()

DEBUG = True
NAME = env('NAME')
USER = env('USER')
PASSWORD = env('PASSWORD')
HOST = env('HOST')
PORT = env('PORT')

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': NAME,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': PORT,
    }
}
