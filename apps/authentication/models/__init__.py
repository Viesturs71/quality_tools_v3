"""
Authentication models initialization.
"""
from .token import Token
from .otp import OneTimePassword

__all__ = ['Token', 'OneTimePassword']
