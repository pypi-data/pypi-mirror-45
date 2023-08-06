import threading


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except ImportError:
    import warnings
    warnings.warn('RPi.GPIO is unavailable, install to use module',
                  category=Warning,
                  stacklevel=2)
    GPIO = None


from pydracs.utils.checks import check_module


class Controller:
    def __init__(self, power_pin):
        check_module(GPIO, 'RPi.GPIO')
        GPIO.setmode(GPIO.BCM)


class InputWatcher:
    def __init__(self,
                 channel,
                 pull_up_down=GPIO.PUD_OFF):
        check_module(GPIO, 'RPi.GPIO')
        GPIO.setup(channel,
                   GPIO.IN,
                   pull_up_down=pull_up_down)
        self._initialize(channel)
        GPIO.add_event_detect(channel,
                              GPIO.BOTH,
                              callback=self._callback)

    def __del__(self):
        self.close()

    @property
    def channel(self):
        return self._channel

    @property
    def input(self):
        self._error_default()
        return GPIO.input(self.channel)

    @property
    def last_input(self):
        return self._previous_input

    @property
    def closed(self):
        return self._closed.is_set()

    def close(self):
        if self.closed:
            return
        GPIO.remove_event_detect(self.channel)
        GPIO.cleanup(self.channel)
        self._set_all()
        self._channel = None

    def is_high(self):
        self._error_default()
        return (self._high.is_set()
                and not self.closed)

    def wait_high(self, timeout=None):
        self._error_default()
        return (self._high.wait(timeout)
                and not self.closed)

    def is_low(self):
        self._error_default()
        return (self._low.is_set()
                and not self.closed)

    def wait_low(self, timeout=None):
        self._error_default()
        return (self._low.wait(timeout)
                and not self.closed)

    def wait_rising(self, timeout=None):
        self._error_default()
        return (self._rise.wait(timeout)
                and not self.closed)

    def wait_falling(self, timeout=None):
        self._error_default()
        return (self._fall.wait(timeout)
                and not self.closed)

    def _initialize(self, channel):
        self._closed = threading.Event()
        self._channel = channel
        self._previous_input = self.input
        self._high = threading.Event()
        self._low = threading.Event()
        if self.last_input is GPIO.HIGH:
            self._high.set()
        else:
            self._low.set()
        self._rise = threading.Event()
        # self._rise.set()
        self._fall = threading.Event()
        # self._fall.set()

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

    def _error_default(self):
        self._error_check('Watcher has been closed')

    def _callback(self, channel):
        # At later date add high/low updater just in case callback fails
        current = self.input
        if  (self.last_input == GPIO.LOW
             and current == GPIO.HIGH):
            self._previous_input = current
            self._set_rise()
        elif (self.last_input == GPIO.HIGH
              and current == GPIO.LOW):
            self._previous_input = current
            self._set_fall()

    def _set_all(self):
        self._closed.set()
        self._high.set()
        self._low.set()
        self._rise.set()
        self._fall.set()

    def _set_rise(self):
        # Signal to all waiting rising calls to unblock
        self._rise.set()
        self._rise.clear()
        # Block all low, Unblock all high
        self._low.clear()
        self._high.set()

    def _set_fall(self):
        # Signal to all waiting falling calls to unblock
        self._fall.set()
        self._fall.clear()
        # Block all high, Unblock all low
        self._high.clear()
        self._low.set()
