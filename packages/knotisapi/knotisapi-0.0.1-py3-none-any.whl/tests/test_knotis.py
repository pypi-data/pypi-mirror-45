from unittest import TestCase
from unittest.mock import create_autospec

from librestapi.client import Response


class TestKnotisApiClass(TestCase):
    def test_knotis_is_defined(self):
        from knotisapi import KnotisApi
        self.assertTrue(KnotisApi)

    def test_knotis_constructor(self):
        from knotisapi import KnotisApi
        kapi = KnotisApi()

        self.assertTrue(kapi)

    def test_password_grant(self):
        from knotisapi import KnotisApi
        kapi = KnotisApi()
        kapi.request = create_autospec(kapi.request)

        response = kapi.password_grant(
            'test_username',
            'test_password'
        )

        self.assertTrue(response)

    def test_refresh_token(self):
        from knotisapi import KnotisApi
        kapi = KnotisApi()
        kapi.request = create_autospec(kapi.request)

        response = kapi.refresh_token(
            'test_token'
        )

        self.assertTrue(response)
        
