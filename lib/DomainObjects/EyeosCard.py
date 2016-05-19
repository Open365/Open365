import json


class EyeosCard:
    def __init__(self, card, signature):
        self._card = card
        self._signature = signature

    def to_headers(self):
        return {
            'card': json.dumps(self._card),
            'signature': self._signature
        }

    def __eq__(self, other):
        return self._card == other._card and self._signature == other._signature
