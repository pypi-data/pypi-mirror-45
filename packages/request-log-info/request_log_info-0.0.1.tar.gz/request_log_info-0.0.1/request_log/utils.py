from logging.handlers import RotatingFileHandler


class RequestRotatingFileLogger(RotatingFileHandler, object):
    def emit(self, record):
        record.ip = record.request.META['REMOTE_ADDR']
        record.path = record.request.path
        record.method = record.request.method
        record.type = 'request'
        record.status_code = ''

        record.data = '{params: ' + str(record.request.GET) + ', data: ' + str(record.request.POST) + '}'
        try:
            response = record.response
            if response:
                record.type = 'response'
                record.status_code = 'status_code:' + str(response.status_code)
                if response.status_code == 200:
                    record.data = '{data: ' + str(response.data) + '}'
                elif response.status_code == 500:
                    record.data = str(response.message)
                else:
                    record.data = '{error: ' + str(response.content, encoding='utf-8') + '}'
        except Exception:
            pass

        super(RequestRotatingFileLogger, self).emit(record)
