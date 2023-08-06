from __future__ import absolute_import

from threading import Thread, Event

from asched_src.asched import BaseScheduler
from asched_src.asched.schedulers.blocking import BlockingScheduler
from asched_src.asched import asbool


class BackgroundScheduler(BlockingScheduler):
    """
    A scheduler that runs in the background using a separate thread
    (:meth:`~asched.schedulers.base.BaseScheduler.start` will return immediately).

    Extra options:

    ========== =============================================================================
    ``daemon`` Set the ``daemon`` option in the background thread (defaults to ``True``, see
               `the documentation
               <https://docs.python.org/3.4/library/threading.html#thread-objects>`_
               for further details)
    ========== =============================================================================
    """

    _thread = None

    def _configure(self, config):
        self._daemon = asbool(config.pop('daemon', True))
        super(BackgroundScheduler, self)._configure(config)

    def start(self, *args, **kwargs):
        self._event = Event()
        BaseScheduler.start(self, *args, **kwargs)
        self._thread = Thread(target=self._main_loop, name='asched')
        self._thread.daemon = self._daemon
        self._thread.start()

    def shutdown(self, *args, **kwargs):
        super(BackgroundScheduler, self).shutdown(*args, **kwargs)
        self._thread.join()
        del self._thread
