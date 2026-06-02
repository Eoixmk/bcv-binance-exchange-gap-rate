import unittest
from unittest.mock import patch

from app.main import read_rates


class ReadRatesTestCase(unittest.TestCase):
    @patch("app.main.get_binance_p2p_rate", return_value=135.2)
    @patch("app.main.get_bcv_rate", return_value=120.5)
    def test_returns_average_when_both_sources_are_available(self, _bcv, _binance):
        response = read_rates()

        self.assertEqual(response["bcv"], 120.5)
        self.assertEqual(response["binance_p2p"], 135.2)
        self.assertEqual(response["promedio"], 127.85)
        self.assertEqual(response["status"], {"bcv": True, "binance_p2p": True})

    @patch("app.main.get_binance_p2p_rate", return_value=135.2)
    @patch("app.main.get_bcv_rate", return_value=None)
    def test_uses_available_rate_when_one_source_fails(self, _bcv, _binance):
        response = read_rates()

        self.assertIsNone(response["bcv"])
        self.assertEqual(response["binance_p2p"], 135.2)
        self.assertEqual(response["promedio"], 135.2)
        self.assertEqual(response["status"], {"bcv": False, "binance_p2p": True})

    @patch("app.main.get_binance_p2p_rate", return_value=None)
    @patch("app.main.get_bcv_rate", return_value=None)
    def test_returns_null_average_when_all_sources_fail(self, _bcv, _binance):
        response = read_rates()

        self.assertIsNone(response["bcv"])
        self.assertIsNone(response["binance_p2p"])
        self.assertIsNone(response["promedio"])
        self.assertEqual(response["status"], {"bcv": False, "binance_p2p": False})


if __name__ == "__main__":
    unittest.main()
