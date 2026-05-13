import json
import unittest
from unittest.mock import patch

from core.updater import LatestRelease, fetch_latest_release, is_newer


class _FakeResponse:
    def __init__(self, payload, status=200):
        self._payload = payload
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        if isinstance(self._payload, bytes):
            return self._payload
        return json.dumps(self._payload).encode("utf-8")


class UpdaterTests(unittest.TestCase):
    def test_is_newer_compares_stable_versions(self):
        self.assertTrue(is_newer("3.7.0", "3.7.1"))
        self.assertFalse(is_newer("3.7.0", "3.7.0"))
        self.assertFalse(is_newer("3.7.0", "3.6.9"))
        self.assertTrue(is_newer("3.7.0", "4.0.0"))

    def test_is_newer_ignores_prerelease_tags(self):
        self.assertFalse(is_newer("3.7.0", "3.7.0-rc1"))
        self.assertFalse(is_newer("3.7.0", "v3.8.0-beta.1"))

    def test_fetch_latest_release_parses_github_response(self):
        payload = {
            "tag_name": "v3.7.1",
            "html_url": "https://github.com/TomBadash/Mouser/releases/tag/v3.7.1",
            "name": "Mouser v3.7.1",
            "published_at": "2026-05-13T00:00:00Z",
        }
        with patch("urllib.request.urlopen", return_value=_FakeResponse(payload)) as mocked:
            release = fetch_latest_release(timeout=1)

        self.assertEqual(
            release,
            LatestRelease(
                tag_name="v3.7.1",
                html_url="https://github.com/TomBadash/Mouser/releases/tag/v3.7.1",
                name="Mouser v3.7.1",
                published_at="2026-05-13T00:00:00Z",
            ),
        )
        request = mocked.call_args.args[0]
        self.assertIn("TomBadash/Mouser", request.full_url)

    def test_fetch_latest_release_returns_none_on_malformed_response(self):
        with patch("urllib.request.urlopen", return_value=_FakeResponse({"tag_name": "v3.7.1"})):
            self.assertIsNone(fetch_latest_release())

    def test_fetch_latest_release_returns_none_on_network_error(self):
        with patch("urllib.request.urlopen", side_effect=OSError("network down")):
            self.assertIsNone(fetch_latest_release())

    def test_fetch_latest_release_returns_none_on_invalid_json(self):
        with patch("urllib.request.urlopen", return_value=_FakeResponse(b"{")):
            self.assertIsNone(fetch_latest_release())


if __name__ == "__main__":
    unittest.main()
