SECRET_KEY = "some-secret-key"
DEBUG = True
ALLOWED_HOSTS = ['192.168.1.105', 'localhost', '127.0.0.1']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'seeyau',
        'USER': 'seeyauapp',
        'PASSWORD': 'database-user-password',
        'HOST': 'localhost',
        'PORT': '3306',
        'TEST': {
            'NAME': 'test_seeyau'
        }
    }
}
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)]
        }
    }
}
