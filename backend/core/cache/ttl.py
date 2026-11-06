"""
Centralized cache timeout configuration for Linklet.
All values are in seconds.
"""


class CacheTTL:
    # Profile caching
    MY_PROFILE = 300          # 5 minutes
    TARGET_PROFILE = 120      # 2 minutes

    # Follow-related caching
    MUTUAL_FOLLOW = 60        # 1 minute
    FOLLOWERS = 60            # 1 minute
    FOLLOWING = 60            # 1 minute

    # Search caching
    USER_SEARCH = 30          # 30 seconds

    # Messaging and notifications
    INBOX = 20                # 20 seconds
    NOTIFICATIONS = 20        # 20 seconds