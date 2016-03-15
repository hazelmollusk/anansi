import logging

logger_path = lambda obj: '.'.join((
    obj.__class__.__module__,
    obj.__class__.__name__,
),)

class LogMixin(object):
    @property
    def logger(self): return logging.getLogger(logger_path(self))

    def log         (s, *a, **k): s.logger.log          (*a, **k)
    def critical    (s, *a, **k): s.logger.critical     (*a, **k)
    def error       (s, *a, **k): s.logger.error        (*a, **k)
    def exception   (s, *a, **k): s.logger.exception    (*a, **k)
    def warning     (s, *a, **k): s.logger.warning      (*a, **k)
    def info        (s, *a, **k): s.logger.info         (*a, **k)
    def debug       (s, *a, **k): s.logger.debug        (*a, **k)