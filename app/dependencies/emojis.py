from enum import Enum


"""
    Aux class to get emojis for beauty console messages :D
"""


class EmojiType(str, Enum):
    SUCCESS = '✅'
    WARNING = '⚠️'
    ERROR = '❌'
    SEARCH = '🔍'
    NO_RESULTS = '🛑'
