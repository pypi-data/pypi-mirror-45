from eve import Eve
from raven.contrib.flask import Sentry
import logging


class SentryEve(Eve):
    """
    Workaround for https://github.com/pyeve/eve/issues/1087
    """

    def __getattr__(self, name):
        if name in {"im_self", "im_func"}:
            raise AttributeError("type object '%s' has no attribute '%s'" %
                                 (self.__class__.__name__, name))
        return super(SentryEve, self).__getattr__(name)

    def __init__(self, name, **kwargs):
        super(SentryEve, self).__init__(name, **kwargs)

        if self.config['SENTRY_DSN']:
            self.sentry = Sentry(self,
                                 dsn=self.config['SENTRY_DSN'],
                                 logging=True,
                                 level=logging.ERROR,
                                 )


__all__ = ['SentryEve', ]
