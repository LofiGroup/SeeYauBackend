from django.test import TestCase
from auth.middleware import TokenAuthMiddleWare


class TestTokenAuthMiddleWare(TestCase):

    def test_token_in_header(self):
        middle_ware = TokenAuthMiddleWare(None)
        token = b"uyusuhduuahsdua"
        scope = {
            "headers": {
                b"Authorization": b"Bearer " + token
            }
        }
        auth_token = middle_ware.get_token_from_header(scope)
        self.assertEqual(token.decode(), auth_token)

    def test_token_in_query(self):
        middle_ware = TokenAuthMiddleWare(None)
        token = b"uyusuhduuahsdua"
        scope = {
            "query_string": b"token=" + token + b"&query=query&random=random"
        }
        auth_token = middle_ware.get_token_from_query(scope)
        self.assertEqual(token.decode(), auth_token)
