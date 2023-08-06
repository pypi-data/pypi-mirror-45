import abc
import threading
import time


from .GPIO import InputWatcher
from .GPIO import GPIO


from pydracs.utils.checks import check_module


class BaseButton(abc.ABC):
    @property
    def closed(self):
        return

    @abc.abstractmethod
    def close(self):
        pass

    @abc.abstractmethod
    def is_pressed(self, timeout=True):
        pass


class GeneralButton(BaseButton):
    def __init__(self,
                 channel,
                 state,
                 pull_up_down=GPIO.PUD_OFF,
                 bouncetime=0,
                 pausetime=0,
                 watcher=None):
        check_module(GPIO, 'RPi.GPIO')
        self._initialize(channel,
                         state,
                         pull_up_down,
                         bouncetime,
                         pausetime,
                         watcher)
        self._thread.start()

    def __del__(self):
        self.close()

    @property
    def channel(self):
        return self._watcher.channel

    @property
    def bouncetime(self):
        return self._btime

    @property
    def pausetime(self):
        return self._ptime

    @property
    def closed(self):
        return self._closed.is_set()

    def close(self):
        if self.closed:
            return
        with self._lock:
            self._closed.set()
            for _ in range(self._queries):
                self._presses.release()
        self._watcher.close()

    def is_pressed(self,
                   timeout=None):
        with self._lock:
            self._error_check_default()
            self._queries += 1
        response = (self._presses.acquire(timeout=timeout)
                    and not self.closed)
        with self._lock:
            self._queries -= 1
        return response

    def _initialize(self,
                    channel,
                    state,
                    pull_up_down,
                    bouncetime,
                    pausetime,
                    watcher):
        self._closed = threading.Event()
        self._lock = threading.Lock()
        self._queries = 0
        self._presses = threading.Semaphore(value=0)
        if watcher is None:
            watcher = InputWatcher(channel,
                                   pull_up_down)
        self._set_watcher(watcher)
        self._set_state(state)
        self._set_bouncetime(bouncetime)
        self._set_pausetime(pausetime)
        self._thread = threading.Thread(target=self._loop,
                                        daemon=True)

    def _set_state(self, state):
        if GPIO.HIGH == state:
            self._edge_callback = self._watcher.wait_falling
            self._reverse_callback = self._watcher.wait_high
        elif GPIO.LOW == state:
            self._edge_callback = self._watcher.wait_rising
            self._reverse_callback = self._watcher.wait_low
        else:
            raise RuntimeError('state must be either'
                               ' GPIO.HIGH or GPIO.LOW, not '
                               + str(state))

    def _set_bouncetime(self, interval):
        if not isinstance(interval, int):
            raise TypeError('int expected, not '
                            + type(interval).__name__)
        elif interval < 0:
            raise ValueError('interval must be non-negative int')
        self._btime = interval

    def _set_pausetime(self, interval):
        if not isinstance(interval, int):
            raise TypeError('int expected, not '
                            + type(interval).__name__)
        elif (interval - self.bouncetime <= 0
              and interval != 0):
            raise ValueError('interval must be larger than bouncetime')
        self._ptime = interval

    def _set_watcher(self, watcher):
        if not isinstance(watcher, InputWatcher):
            raise TypeError('InputWatcher expected, not '
                            + type(watcher).__name__)
        self._watcher = watcher

    def _press(self):
        return self._edge_callback()

    def _debounce(self):
        time.sleep(self.bouncetime / 1000)

    def _pause(self):
        if self._ptime <= 0:
            return True
        return not self._reverse_callback((self._ptime - self._btime) / 1000)

    def _depress(self) -> bool:
        return self._reverse_callback()

    def _loop(self):
        try:
            while True:
                if self.closed:
                    break
                if not self._press():
                    continue
                self._debounce()
                if not self._pause():
                    continue
                if not self._depress():
                    continue
                self._presses.release()
        except RuntimeError:
            pass
        finally:
            self.close()

    def _error_check(self, *messages):
        if not self.closed:
            return
        # Build message like print
        err = ''
        for i, message in enumerate(messages):
            if i+1 == len(messages):
                err += message
            else:
                err += message+' '
        raise RuntimeError(err)

    def _error_check_default(self):
        self._error_check('Button has been closed')


class Button(GeneralButton):
    def __init__(self,
                 channel,
                 state,
                 pull_up_down=GPIO.PUD_OFF,
                 bouncetime=0,
                 watcher=None):
        super().__init__(channel,
                         state,
                         pull_up_down,
                         bouncetime=bouncetime,
                         watcher=watcher)


class LongButton(GeneralButton):
    def __init__(self,
                 channel,
                 state,
                 pull_up_down=GPIO.PUD_OFF,
                 bouncetime=0,
                 watcher=None):
        super().__init__(channel,
                         state,
                         pull_up_down,
                         bouncetime=bouncetime,
                         pausetime=3000,
                         watcher=watcher)
