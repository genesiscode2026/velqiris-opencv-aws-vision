"""
AWS Lambda Serverless Function for VELQIRIS OpenCV 5 Market Truth Inspection
===========================================================================
Handler for API Gateway HTTP API and S3 ObjectCreated events.
Deploys on AWS Lambda with OpenCV 5 Container / Layer.
"""

import base64
import json
from typing import Any, Dict
from opencv_market_vision import ChartVisionInspector


def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    AWS Lambda entry point.
    Accepts:
    - API Gateway POST with base64 image or JSON metadata in body
    - Direct invocation payload
    """
    inspector = ChartVisionInspector(fail_closed=True)

    try:
        # Check if invocation comes from API Gateway
        body_raw = event.get("body")
        is_base64 = event.get("isBase64Encoded", False)

        image_bytes = None
        metadata = None

        if body_raw:
            if is_base64:
                image_bytes = base64.b64decode(body_raw)
            else:
                try:
                    payload = json.loads(body_raw)
                    if "image_base64" in payload:
                        image_bytes = base64.b64decode(payload["image_base64"])
                    metadata = payload.get("chart_metadata", payload)
                except json.JSONDecodeError:
                    return {
                        "statusCode": 400,
                        "headers": {"Content-Type": "application/json"},
                        "body": json.dumps({"error": "INVALID_JSON_BODY"}),
                    }
        elif "chart_metadata" in event:
            metadata = event["chart_metadata"]
        elif "image_base64" in event:
            image_bytes = base64.b64decode(event["image_base64"])
        else:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "MISSING_CHART_PAYLOAD", "message": "Provide image_base64 or chart_metadata."}),
            }

        result = inspector.inspect_chart(image_bytes=image_bytes, chart_metadata=metadata)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "X-Velqiris-Evidence-Type": "OPENCV5_VISUAL_TRUTH",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(result, indent=2),
        }

    except ValueError as ve:
        return {
            "statusCode": 422,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "FAIL_CLOSED_VALIDATION_ERROR", "error": str(ve)}),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "INTERNAL_VISION_ERROR", "error": str(e)}),
        }
