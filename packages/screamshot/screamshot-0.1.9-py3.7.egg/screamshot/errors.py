"""
Exceptions for screamshot package.
"""


class ScreamshotError(Exception):
    """
    Base exception for screamshot.
    """


class BadUrl(ScreamshotError):
    """
    Bad url exception
    """
