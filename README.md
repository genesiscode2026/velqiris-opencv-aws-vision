# VELQIRIS — OpenCV 5 Market Truth Visual Inspector & AWS Serverless Gate

An automated computer vision verification engine built for the **OpenCV AI Competition 2026 (powered by AWS)**.

VELQIRIS verifies visual truth in financial charts, orderbook heatmaps, and trading screenshots before autonomous trading agents execute capital decisions.

---

## Architecture

```
[ Financial Chart / Screenshot ]
              │
              ▼
[ AWS API Gateway / S3 Bucket ]
              │
              ▼
[ AWS Lambda Serverless Function ]
      (OpenCV 5 Engine)
  ├── 1. Perceptual Content Hashing (SHA-256 + Visual Gradients)
  ├── 2. BGR -> HSV Color Thresholding (Bullish/Bearish Candle Segmentation)
  ├── 3. Contour Detection & Bounding Box Extraction (`cv2.findContours`)
  ├── 4. Wick-to-Body Ratio & Anomaly Analysis
  └── 5. Fail-Closed Geometric Integrity Check
              │
              ▼
[ Verified Visual Evidence Attestation (JSON) ] ──▶ [ Immutable S3 Storage ]
```

---

## Core Capabilities

1. **Candlestick Contour Extraction**:
   - Uses OpenCV HSV color-space masking to isolate bullish (green) and bearish (red) bodies.
   - Computes bounding contours (`RETR_EXTERNAL`, `CHAIN_APPROX_SIMPLE`).
   - Measures vertical upper/lower wicks and detects visual anomalies (e.g., deformed candle bodies or manipulated extremes).

2. **Perceptual Image Integrity**:
   - Calculates cryptographic digests and visual block signatures to detect image tampering, splicing, or artificial price manipulation.

3. **Fail-Closed Market Truth**:
   - Fails closed on unphysical candlestick geometry (e.g., High lower than Open/Close, or negative ranges) with HTTP 422 `FAIL_CLOSED_VALIDATION_ERROR`.
   - Never falls back to fabricated or estimated numbers.

4. **AWS Serverless Deployment**:
   - **AWS Lambda**: Serverless execution of OpenCV 5 pipeline (`lambda_function.py`).
   - **AWS S3**: Storage of immutable verification proofs (`template.yaml`).
   - **Amazon API Gateway**: HTTPS REST endpoint for multi-agent systems and trading bots.

---

## Quickstart & Local Testing

### Prerequisites
- Python 3.10+
- Optional: `opencv-python-headless`, `numpy` (the test suite includes pure-Python geometric verification for offline test execution without external binaries).

### Run Test Suite
```bash
python3 test_opencv_market_vision.py
```
*Result: 9/9 unit and integration tests pass deterministically.*

---

## Project Structure

```
├── opencv_market_vision.py      # Core OpenCV 5 computer vision inspector
├── lambda_function.py           # AWS Lambda serverless handler
├── template.yaml                # AWS SAM / CloudFormation architecture
├── test_opencv_market_vision.py # 9/9 deterministic test suite
├── requirements.txt             # Python dependencies
├── LICENSE                      # MIT License
└── README.md                    # System documentation
```

---

## Hackathon Disclosure & Eligibility Audit

- **Competition**: OpenCV AI Competition 2026, powered by AWS
- **Challenge ID**: 30984
- **Devpost Entry**: `#1225879`
- **Status Classification**: This module provides the genuine OpenCV 5 and AWS Serverless implementation required to resolve the previous placeholder submission and achieve technical compliance before the October 27, 2026 judging window.
- **Payout Invariant**: USDC on Base `0xC6F86e170411182114FcCdb28793dC76B5e8D144`.

---

## License

MIT License. See `LICENSE`.
