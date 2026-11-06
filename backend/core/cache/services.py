"""
Reusable cache operations for Linklet.
"""

import logging

from django.core.cache import cache

logger = logging.getLogger(__name__)


def get_cached_data(key, default=None):
    """
    Retrieve data from cache.
    Returns default if the key does not exist or cache is unavailable.
    """

    try:
        return cache.get(key, default)

    except Exception:
        logger.exception("Linklet cache read failed: %s", key)
        return default


def set_cached_data(key, data, timeout=None):
    """
    Save data to cache.
    """

    try:
        return cache.set(key, data, timeout)

    except Exception:
        logger.exception("Linklet cache write failed: %s", key)
        return False


def delete_cached_data(key):
    """
    Delete a specific cache entry.
    """

    try:
        return cache.delete(key)

    except Exception:
        logger.exception("Linklet cache deletion failed: %s", key)
        return False


def get_or_set_cached_data(key, callback, timeout=None):
    """
    Return cached data if available.

    Otherwise, execute callback, cache its result,
    and return the result.

    Database operations should be inside callback.
    """

    cached_data = get_cached_data(key)

    if cached_data is not None:
        return cached_data

    fresh_data = callback()

    set_cached_data(key, fresh_data, timeout)

    return fresh_data