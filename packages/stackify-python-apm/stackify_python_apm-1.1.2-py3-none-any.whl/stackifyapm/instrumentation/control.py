import threading

from stackifyapm.instrumentation import register

_lock = threading.Lock()


def instrument(config_file=None):
    """
    Instruments all registered methods/functions
    """
    with _lock:
        for obj in register.get_instrumentation_objects():
            obj.instrument(config_file=config_file)


def uninstrument(config_file=None):
    """
    If instrumentation is present, remove it and replaces it with the original method/function
    """
    with _lock:
        for obj in register.get_instrumentation_objects():
            obj.uninstrument(config_file=config_file)
