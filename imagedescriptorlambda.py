import json
import boto3
import base64
import re
import uuid

# Initialize AWS Clients
client = boto3.client("bedrock-runtime", region_name="us-east-1")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("ImageDescriptions")  # Change table name if needed

# Claude 3 Haiku Model ID
MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"

def lambda_handler(event, context):
    try:
        # Parse request body safely
        body = json.loads(event.get("body", "{}"))
        image_data = body.get("image_base64", "").strip()

        if not image_data:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing base64-encoded image data"})
            }

        # Clean base64 string
        image_data = re.sub(r"\s+", "", image_data)

        # Validate base64 encoding
        try:
            base64.b64decode(image_data, validate=True)
        except Exception:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid base64 image data"})
            }

        # Construct the request payload for Bedrock
        request_payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 300,
            "temperature": 0.7,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this image in detail."},
                        {"type": "image", "source": {
                            "type": "base64",
                            "media_type": "image/png",  # Adjust if needed
                            "data": image_data
                        }}
                    ]
                }
            ],
        }

        # Convert request to JSON
        request_json = json.dumps(request_payload, ensure_ascii=False)

        # Invoke Amazon Bedrock model
        response = client.invoke_model(
            modelId=MODEL_ID,
            body=request_json
        )

        # Ensure response body exists
        if "body" not in response:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "No response body received from Bedrock"})
            }

        # Read response body safely
        response_body = response["body"]
        response_text = response_body.read().decode("utf-8")
        response_data = json.loads(response_text)

        # Extract AI-generated description
        description = response_data.get("content", [{}])[0].get("text", "No description generated.")

        # Generate a unique ID for this image
        image_id = str(uuid.uuid4())

        # Store result in DynamoDB
        table.put_item(
            Item={
                "ImageID": image_id,
                "Description": description
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"ImageID": image_id, "Description": description})
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON request format"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
