import functools
import requests
import copy


class EyeosApiCall:
    """Class that wraps the requests library but adds some utility related to eyeos. For now it accepts EyeosCard
    objects and adds them to the headers.
    """
    def __init__(self):
        requests.packages.urllib3.disable_warnings()

    def __dir__(self):
        """Override dir(), returning requests' dir()"""
        return dir(requests)

    def __getattr__(self, item):
        """forward all attribute or method accesses to requests"""
        wrapped = None
        try:
            wrapped = getattr(requests, item)
        except AttributeError as e:
            raise AttributeError("'{0}' has no attribute '{1}'".format(self.__class__.__name__, item)) from e

        if not callable(wrapped):
            # If the attribute exists but is not callable, we can't wrap it in a function, return it directly
            return wrapped

        # Wrap the method with a function that converts the card (if present) to headers
        @functools.wraps(wrapped)
        def wrapper(*args, card=None, **kwargs):
            if card:
                kwargs = copy.deepcopy(kwargs)
                if 'headers' not in kwargs:
                    kwargs['headers'] = {}
                kwargs['headers'].update(card.to_headers())

            return wrapped(*args, **kwargs)

        return wrapper
