from django.test import TestCase
from django.core.cache import cache

from core.cache.keys import (
    my_profile_key,
    target_profile_key,
)

from core.cache.services import (
    get_cached_data,
    set_cached_data,
    delete_cached_data,
    get_or_set_cached_data,
)


class LinkletCacheTests(TestCase):

    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    def test_cache_set_and_get(self):
        key = my_profile_key(1)

        set_cached_data(key, {"username": "harshal"}, 60)

        result = get_cached_data(key)

        self.assertEqual(result["username"], "harshal")

    def test_cache_delete(self):
        key = my_profile_key(1)

        set_cached_data(key, {"username": "harshal"}, 60)

        delete_cached_data(key)

        self.assertIsNone(get_cached_data(key))

    def test_user_cache_keys_are_different(self):
        user_one = my_profile_key(1)
        user_two = my_profile_key(2)

        self.assertNotEqual(user_one, user_two)

    def test_target_profile_keys_are_requester_specific(self):
        key_one = target_profile_key(1, "john")
        key_two = target_profile_key(2, "john")

        self.assertNotEqual(key_one, key_two)

    def test_get_or_set_executes_callback(self):
        key = my_profile_key(10)

        result = get_or_set_cached_data(
            key,
            lambda: {"username": "test_user"},
            60,
        )

        self.assertEqual(result["username"], "test_user")

        cached_result = get_cached_data(key)

        self.assertEqual(cached_result["username"], "test_user")