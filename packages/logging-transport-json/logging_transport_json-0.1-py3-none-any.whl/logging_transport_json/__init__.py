from logging.handlers import SocketHandler, DatagramHandler
import json


class JsonSocketHandler(SocketHandler):
    def emit(self, record):
        try:
            d = dict(record.__dict__)
            d['msg'] = record.getMessage()
            d['args'] = None
            d['exc_info'] = None
            # Issue #25685: delete 'message' if present: redundant with 'msg'
            d.pop('message', None)
            self.send(json.dumps(d).encode())
        except Exception:
            self.handleError(record)


class JsonDatagramHandler(DatagramHandler):
    def emit(self, record):
        try:
            d = dict(record.__dict__)
            d['msg'] = record.getMessage()
            d['args'] = None
            d['exc_info'] = None
            # Issue #25685: delete 'message' if present: redundant with 'msg'
            d.pop('message', None)
            self.send(json.dumps(d).encode())
        except Exception:
            self.handleError(record)
