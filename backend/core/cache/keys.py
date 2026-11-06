"""
Centralized cache key generation for Linklet.
"""

import hashlib
import json


CACHE_NAMESPACE = "linklet"


def build_cache_key(namespace: str, *parts) -> str:
    """
    Generate a consistent, unique cache key.

    Example:
    linklet:profile:my-profile:<user-hash>
    """

    payload = json.dumps(
        parts,
        sort_keys=True,
        default=str,
        separators=(",", ":"),
    )

    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]

    return f"{CACHE_NAMESPACE}:{namespace}:{digest}"


def my_profile_key(user_id):
    return build_cache_key("profile:me", user_id)


def target_profile_key(requester_id, username):
    return build_cache_key(
        "profile:target",
        requester_id,
        username,
    )


def mutual_follow_key(user_id):
    return build_cache_key("follow:mutual", user_id)


def followers_key(user_id):
    return build_cache_key("follow:followers", user_id)


def following_key(user_id):
    return build_cache_key("follow:following", user_id)


def user_search_key(user_id, query):
    return build_cache_key(
        "profile:search",
        user_id,
        query.strip().lower(),
    )


def inbox_key(user_id):
    return build_cache_key("messaging:inbox", user_id)


def notification_history_key(user_id):
    return build_cache_key("notification:history", user_id)