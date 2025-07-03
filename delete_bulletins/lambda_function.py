import boto3
import json

SECRET_NAME = "church-bulletin-bot/credentials"

def get_secret(secret_name):
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

def lambda_handler(event, context):
    # Load secrets
    secret = get_secret(SECRET_NAME)
    s3_bucket = secret["s3_bucket"]

    s3 = boto3.client("s3")
    prefix = "bulletins/"

    print(f"🔍 Listing objects in s3://{s3_bucket}/{prefix}")
    response = s3.list_objects_v2(Bucket=s3_bucket, Prefix=prefix)

    if "Contents" not in response:
        return {"statusCode": 200, "message": "✅ Nothing to delete."}

    objects_to_delete = [{"Key": obj["Key"]} for obj in response["Contents"]]

    print(f"🗑️ Deleting {len(objects_to_delete)} objects...")
    delete_response = s3.delete_objects(
        Bucket=s3_bucket,
        Delete={"Objects": objects_to_delete}
    )

    deleted = delete_response.get("Deleted", [])
    errors = delete_response.get("Errors", [])

    return {
        "statusCode": 200,
        "message": f"✅ Deleted {len(deleted)} objects. ❌ Errors: {len(errors)}",
        "deleted_keys": [obj["Key"] for obj in deleted]
    }