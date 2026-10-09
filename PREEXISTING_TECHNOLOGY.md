# PRE-EXISTING TECHNOLOGY & IP DISCLOSURE
**Competition:** OpenCV AI Competition 2026 (OpenCV + AWS) (Devpost #1225879)  
**Project:** VELQIRIS OpenCV 5 Market Truth Visual Inspector  

---

## 1. PRE-EXISTING FOUNDATIONAL TECHNOLOGY
- **VELQIRIS Market Truth Invariants:** Quantitative bounds on acceptable market data and fail-closed security logic.
- **Open Source Libraries:** Python standard library (`hashlib`, `json`, `math`, `unittest`), MIT licensed.

---

## 2. WORK CREATED SPECIFICALLY FOR THIS HACKATHON
- **OpenCV 5 Computer Vision Engine (`opencv_market_vision.py`):** Authored specifically for this hackathon with contour extraction, morphological noise filtration, and CandlestickMetric geometry calculations.
- **Dual-Engine Architecture:** Engineered to switch seamlessly between OpenCV native C++ acceleration and deterministic pure-Python execution for friction-free judge evaluation.
- **AWS Serverless SAM Template (`template.yaml`):** Production SAM infrastructure template for AWS Lambda and API Gateway deployment.
- **AWS Lambda Handler (`lambda_function.py`):** Serverless wrapper handling base64 payload decoding and structured JSON emission.
- **Test Suite (`test_opencv_market_vision.py`):** 9 deterministic unit and integration tests.

---

## 3. COMPLIANCE & ELIGIBILITY ATTESTATION
All computer vision code, AWS Lambda handlers, and SAM deployment definitions were authored specifically during the OpenCV AI Competition window under MIT license.
