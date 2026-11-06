"""
Centralized cache invalidation for Linklet.
"""

from .keys import (
    my_profile_key,
    mutual_follow_key,
    followers_key,
    following_key,
    inbox_key,
    notification_history_key,
)

from .services import delete_cached_data
from .keys import target_profile_key


def invalidate_profile_cache(user_id):
    """Invalidate the user's own profile cache."""

    delete_cached_data(my_profile_key(user_id))


def invalidate_follow_cache(user_id):
    """Invalidate follow-related caches for a user."""

    keys = [
        mutual_follow_key(user_id),
        followers_key(user_id),
        following_key(user_id),
    ]

    for key in keys:
        delete_cached_data(key)


def invalidate_inbox_cache(user_id):
    """Invalidate the user's inbox cache."""

    delete_cached_data(inbox_key(user_id))


def invalidate_notification_cache(user_id):
    """Invalidate notification history cache."""

    delete_cached_data(notification_history_key(user_id))


def invalidate_target_profile_cache(requester_id, username):
    """
    Invalidate a target profile cached for a specific requester.
    """

    delete_cached_data(
        target_profile_key(requester_id, username)
    )