from .emitter import Emitter

from .strings import StringValidator
from .numbers import NumberValidator
from .booleans import BooleanValidator


class Validator(Emitter, StringValidator, NumberValidator, BooleanValidator):
    def __init__(self):
        super().__init__()
