# JUDGE START HERE — VELQIRIS OPENCV 5 & AWS SERVERLESS INSPECTOR
**Hackathon:** OpenCV AI Competition 2026 (OpenCV + AWS) (Devpost #1225879)  
**Track:** OpenCV 5 + AWS Serverless Architecture  
**Verification Time:** < 10 seconds  

---

## 1. What Is This Project?
An institutional-grade computer vision inspector that detects visual fabrication, synthetic candle injection, and wick anomalies in financial charts. Built with a dual-engine architecture supporting both accelerated OpenCV 5 (`cv2`) C++ pipelines in AWS Lambda containers and zero-dependency fallbacks for offline testing.

---

## 2. Quick Verification (Run in 1 Command)

```bash
# Run the complete test suite (9 tests covering geometry, perceptual hashes, and Lambda handlers)
python3 -m unittest -v test_opencv_market_vision.py
```

### Expected Output:
```
test_empty_image_raises_error ... ok
test_fail_closed_on_unphysical_geometry ... ok
test_perceptual_hash_determinism ... ok
test_synthetic_candlestick_analysis ... ok
test_wick_anomaly_detection ... ok
test_lambda_fail_closed_geometry_validation ... ok
test_lambda_invalid_json ... ok
test_lambda_missing_body ... ok
test_lambda_successful_json_invocation ... ok

Ran 9 tests in 0.000s
OK
```

---

## 3. Key Deliverables & Documentation

- [Reproducibility & Benchmark Report](./OPENCV_REPRODUCIBILITY_REPORT.md)
- [Devpost Submission Packet](./DEVPOST_SUBMISSION_PACKET.md)
- [AWS SAM Template](./template.yaml)
- [AWS Lambda Handler](./lambda_function.py)
- [Pre-Existing Technology Disclosure](./PREEXISTING_TECHNOLOGY.md)
- [Verification Evidence Log](./VERIFICATION_EVIDENCE.md)
