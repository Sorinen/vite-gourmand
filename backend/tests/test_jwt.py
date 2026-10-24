import os
import unittest
from unittest import mock

from app.utils import jwt as jwt_utils


class JwtSecretKeyTests(unittest.TestCase):
    def test_absent_key_raises(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError):
                jwt_utils.create_access_token({"sub": "a@b.c"})
            with self.assertRaises(RuntimeError):
                jwt_utils.verify_token("x.y.z")
            with self.assertRaises(RuntimeError):
                jwt_utils.get_secret_key()

    def test_empty_or_blank_key_raises(self):
        for value in ("", "   "):
            with mock.patch.dict(os.environ, {"SECRET_KEY": value}, clear=True):
                with self.assertRaises(RuntimeError):
                    jwt_utils.create_access_token({"sub": "a@b.c"})

    def test_valid_key_roundtrip(self):
        with mock.patch.dict(os.environ, {"SECRET_KEY": "cle-de-test"}, clear=True):
            token = jwt_utils.create_access_token({"sub": "a@b.c"})
            self.assertEqual(jwt_utils.verify_token(token)["sub"], "a@b.c")

    def test_token_signed_with_other_key_rejected(self):
        with mock.patch.dict(os.environ, {"SECRET_KEY": "cle-un"}, clear=True):
            token = jwt_utils.create_access_token({"sub": "a@b.c"})
        with mock.patch.dict(os.environ, {"SECRET_KEY": "cle-deux"}, clear=True):
            self.assertIsNone(jwt_utils.verify_token(token))

    def test_old_hardcoded_fallback_not_accepted(self):
        forged = jwt_utils.jwt.encode({"sub": "admin@x.y"}, "changez_moi_en_production", algorithm="HS256")
        with mock.patch.dict(os.environ, {"SECRET_KEY": "cle-de-test"}, clear=True):
            self.assertIsNone(jwt_utils.verify_token(forged))


if __name__ == "__main__":
    unittest.main()
