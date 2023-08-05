from logging.handlers import RotatingFileHandler


class RequestRotatingFileLogger(RotatingFileHandler, object):
    def emit(self, record):
        record.ip = '0.0.0.0'
        record.path = record.request.path
        record.method = record.request.method
        record.type = 'request'

        record.data = '{params: ' + str(record.request.GET) + ', data: ' + str(record.request.POST) + '}'
        try:
            record.ip = record.request.META['REMOTE_ADDR']
        except Exception:
            pass

        super(RequestRotatingFileLogger, self).emit(record)
