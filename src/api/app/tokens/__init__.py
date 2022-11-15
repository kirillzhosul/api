"""
    API tokens.
    Provides class interfaces for working with tokens.
    Provides base class `base_token.BaseToken` for implementation of own token type.
    All tokens should be child classes of BaseToken class.
"""


from .base_token import BaseToken
from .access_token import AccessToken
from . import exceptions

__all__ = [
    "BaseToken",
    "AccessToken",
    "exceptions"
]