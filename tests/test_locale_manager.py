import unittest

from ui.locale_manager import _TRANSLATIONS


class LocaleManagerTranslationTests(unittest.TestCase):
    def test_key_capture_error_messages_exist_in_all_locales(self):
        required = {
            "key_capture.error.unsupported_key",
            "key_capture.error.unknown_key",
            "key_capture.error.duplicate_key",
            "key_capture.error.multiple_main_keys",
            "key_capture.error.missing_main_key",
            "key_capture.error.empty_segment",
            "key_capture.error.unsupported",
        }

        for locale, strings in _TRANSLATIONS.items():
            with self.subTest(locale=locale):
                self.assertTrue(required.issubset(strings))
                for key in required:
                    self.assertTrue(strings[key].strip())

    def test_update_install_messages_exist_in_all_locales(self):
        required = {
            "scroll.update_idle",
            "scroll.update_available",
            "scroll.update_checking",
            "scroll.update_downloading",
            "scroll.update_verifying",
            "scroll.update_ready",
            "scroll.update_installing",
            "scroll.update_installed",
            "scroll.update_installed_version",
            "scroll.update_cancelled",
            "scroll.update_manual",
            "scroll.update_manual_windows",
            "scroll.update_manual_macos",
            "scroll.update_manual_linux",
            "scroll.update_no_asset",
            "scroll.update_error",
            "scroll.update_error_check_first",
            "scroll.update_error_network_error",
            "scroll.update_error_metadata_missing",
            "scroll.update_error_metadata_invalid",
            "scroll.update_error_permission_denied",
            "scroll.update_error_file_error",
            "scroll.update_error_install_failed",
            "scroll.update_error_sha256_mismatch",
            "scroll.update_error_size_mismatch",
            "scroll.update_error_expired_metadata",
            "scroll.update_error_older_build",
            "scroll.update_check",
            "scroll.update_download",
            "scroll.update_cancel",
            "scroll.update_verify",
            "scroll.update_install",
            "scroll.update_open_release",
        }

        for locale, strings in _TRANSLATIONS.items():
            with self.subTest(locale=locale):
                self.assertTrue(required.issubset(strings))
                for key in required:
                    self.assertTrue(strings[key].strip())


if __name__ == "__main__":
    unittest.main()
