import warnings


def check_module(module, name):
    if module is not None:
        return
    message = name
    message += ' module unavailable, install to use'
    raise RuntimeError(message)
