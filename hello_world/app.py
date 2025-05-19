import json
import boto3
import os
import uuid

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    method = event["httpMethod"]

    if method == "POST":
        body = json.loads(event["body"])
        task_id = str(uuid.uuid4())
        task_item = {
            "taskId": task_id,
            "title": body["title"],
            "status": body.get("status", "pending")
        }
        table.put_item(Item=task_item)
        return response(200, {"message": "Task created", "task": task_item})

    elif method == "GET":
        tasks = table.scan()
        return response(200, {"tasks": tasks["Items"]})

    elif method == "DELETE":
        body = json.loads(event["body"])
        task_id = body["taskId"]
        table.delete_item(Key={"taskId": task_id})
        return response(200, {"message": "Task deleted", "taskId": task_id})

    return response(400, {"message": "Unsupported method"})

def response(status_code, body):
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
        "headers": {"Content-Type": "application/json"}
    }
