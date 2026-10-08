"""
Unit & Integration Tests for VELQIRIS OpenCV 5 Market Truth Visual Inspector
============================================================================
Runs deterministically offline without external network dependencies.
"""

import json
import unittest
from opencv_market_vision import ChartVisionInspector, CandlestickMetric
from lambda_function import lambda_handler


class TestChartVisionInspector(unittest.TestCase):

    def setUp(self):
        self.inspector = ChartVisionInspector(fail_closed=True)

    def test_perceptual_hash_determinism(self):
        sample_bytes = b"sample_png_chart_image_payload_bytes_12345"
        hash1 = self.inspector.compute_perceptual_hash(sample_bytes)
        hash2 = self.inspector.compute_perceptual_hash(sample_bytes)
        self.assertEqual(hash1, hash2)
        self.assertEqual(len(hash1), 64)  # SHA-256 hex length

    def test_empty_image_raises_error(self):
        with self.assertRaises(ValueError):
            self.inspector.compute_perceptual_hash(b"")

    def test_synthetic_candlestick_analysis(self):
        chart_metadata = {
            "synthetic_candles": [
                {"open": 100.0, "close": 105.0, "high": 107.0, "low": 98.0},   # Bullish
                {"open": 105.0, "close": 101.0, "high": 106.0, "low": 100.0},  # Bearish
                {"open": 101.0, "close": 101.0, "high": 103.0, "low": 99.0},   # Doji
            ]
        }
        result = self.inspector.inspect_chart(chart_metadata=chart_metadata)
        self.assertEqual(result["status"], "VERIFIED_VISUAL_TRUTH")
        self.assertEqual(result["total_candles_detected"], 3)
        self.assertEqual(result["distribution"]["bullish"], 1)
        self.assertEqual(result["distribution"]["bearish"], 1)
        self.assertEqual(result["distribution"]["doji"], 1)
        self.assertTrue(result["visual_integrity_verified"])

    def test_fail_closed_on_unphysical_geometry(self):
        # High is below open and close -> impossible in physical market
        corrupt_metadata = {
            "synthetic_candles": [
                {"open": 100.0, "close": 105.0, "high": 95.0, "low": 90.0}
            ]
        }
        with self.assertRaises(ValueError) as ctx:
            self.inspector.inspect_chart(chart_metadata=corrupt_metadata)
        self.assertIn("UNPHYSICAL_CANDLE_GEOMETRY", str(ctx.exception))

    def test_wick_anomaly_detection(self):
        # Body is tiny (0.1), range is huge (20) -> ratio < 0.05
        anomaly_metadata = {
            "synthetic_candles": [
                {"open": 100.0, "close": 100.1, "high": 110.0, "low": 90.0}
            ]
        }
        result = self.inspector.inspect_chart(chart_metadata=anomaly_metadata)
        self.assertFalse(result["visual_integrity_verified"])
        self.assertTrue(len(result["anomalies_detected"]) > 0)
        self.assertIn("EXTREME_WICK_ANOMALY", result["anomalies_detected"][0])


class TestLambdaHandler(unittest.TestCase):

    def test_lambda_successful_json_invocation(self):
        event = {
            "body": json.dumps({
                "chart_metadata": {
                    "synthetic_candles": [
                        {"open": 68000.0, "close": 68500.0, "high": 68900.0, "low": 67800.0},
                        {"open": 68500.0, "close": 68200.0, "high": 68600.0, "low": 68100.0},
                    ]
                }
            })
        }
        response = lambda_handler(event)
        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["status"], "VERIFIED_VISUAL_TRUTH")
        self.assertEqual(body["total_candles_detected"], 2)

    def test_lambda_missing_body(self):
        event = {}
        response = lambda_handler(event)
        self.assertEqual(response["statusCode"], 400)
        body = json.loads(response["body"])
        self.assertEqual(body["error"], "MISSING_CHART_PAYLOAD")

    def test_lambda_invalid_json(self):
        event = {"body": "invalid{json[not_closed"}
        response = lambda_handler(event)
        self.assertEqual(response["statusCode"], 400)
        body = json.loads(response["body"])
        self.assertEqual(body["error"], "INVALID_JSON_BODY")

    def test_lambda_fail_closed_geometry_validation(self):
        event = {
            "body": json.dumps({
                "chart_metadata": {
                    "synthetic_candles": [
                        {"open": 100.0, "close": 105.0, "high": 80.0, "low": 70.0}
                    ]
                }
            })
        }
        response = lambda_handler(event)
        self.assertEqual(response["statusCode"], 422)
        body = json.loads(response["body"])
        self.assertEqual(body["status"], "FAIL_CLOSED_VALIDATION_ERROR")


if __name__ == "__main__":
    unittest.main()
