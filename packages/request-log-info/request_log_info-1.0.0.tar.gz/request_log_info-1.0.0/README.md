# request_log_info

## Installing

```bash
$ pip install request-log-info
```

Then add ```request_log.middleware.LoggingMiddleware``` to your ```MIDDLEWARE```.

For example:

```python
MIDDLEWARE = (
    ...,   
    'request_log.middleware.LoggingMiddleware',
    ...,
)
```

And configure logging in your app:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'request': {
            'format': '%(type)s' + '[%(asctime)s]' + ' ip:%(ip)s,' + ' url:%(path)s,' +
                      ' method:%(method)s, ' + '%(data)s '
        },
    },
    'handlers': {
        'info': {
            'class': 'request_log.utils.RequestRotatingFileLogger',
            'formatter': 'request'
        },
    },
    'loggers': {
        'request': {
            'level': 'DEBUG',  # change debug level as appropiate
            'handlers': ['info'],
            'propagate': False,
        },
    },
}
```
