import json
import os
import uuid
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Key

# ================================
# CONFIG (SAFE FOR PUBLIC REPO)
# ================================

TABLE_NAME = os.environ.get("DIARY_TABLE_NAME", "REPLACE_ME")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

# ================================
# HANDLER
# ================================

def lambda_handler(event, context):
    method = event["requestContext"]["http"]["method"]

    # Auth context (implementation depends on authorizer)
    user_id = get_user_id(event)
    if not user_id:
        return response_builder(401, {"message": "Unauthorized"})

    if method == "GET":
        return get_entries(user_id)

    if method == "POST":
        return create_entry(user_id, event)

    if method == "DELETE":
        return delete_entry(user_id, event)

    return response_builder(400, {"message": "Unsupported method"})


# ================================
# OPERATIONS
# ================================

def get_entries(user_id):
    response = table.query(
        KeyConditionExpression=Key("UserID").eq(user_id)
    )
    return response_builder(200, response.get("Items", []))


def create_entry(user_id, event):
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return response_builder(400, {"message": "Invalid JSON"})

    content = sanitize_content(body.get("content", ""))

    entry_id = str(uuid.uuid4())

    table.put_item(
        Item={
            "UserID": user_id,
            "EntryID": entry_id,
            "Content": content,
            "CreatedAt": datetime.utcnow().isoformat()
        }
    )

    return response_builder(200, {"message": "Saved successfully"})


def delete_entry(user_id, event):
    entry_id = event.get("pathParameters", {}).get("id")
    if not entry_id:
        return response_builder(400, {"message": "Missing entry id"})

    table.delete_item(
        Key={
            "UserID": user_id,
            "EntryID": entry_id
        }
    )

    return response_builder(200, {"message": "Deleted successfully"})


# ================================
# HELPERS
# ================================

def get_user_id(event):
    """
    Extract user ID from authorizer context.
    Implementation intentionally abstracted
    for public repository safety.
    """
    try:
        return event["requestContext"]["authorizer"]["jwt"]["claims"]["sub"]
    except KeyError:
        return None


def sanitize_content(content):
    """
    Placeholder for server-side sanitization.
    Always sanitize on backend even if frontend does.
    """
    if not isinstance(content, str):
        return ""
    return content.strip()


def response_builder(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "GET,POST,DELETE"
        },
        "body": json.dumps(body)
    }
