import boto3
import requests
import datetime
import json

# === Configuration ===
SECRET_NAME = "church-bulletin-bot/credentials"

# === Helpers ===
def get_secret(secret_name):
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

def lambda_handler(event, context):
    # Step 1: Load config from Secrets Manager
    secret = get_secret(SECRET_NAME)
    url_prefix = secret["bulletin_url_prefix"]
    s3_bucket = secret["s3_bucket"]

    # Step 2: Construct URL and S3 key
    today = datetime.date.today()
    date_str = today.strftime("%Y%m%d")
    pdf_url = f"{url_prefix}{date_str}B.pdf"
    s3_key = f"bulletins/bulletin_{date_str}.pdf"

    print(f"📥 Downloading PDF from {pdf_url}")
    response = requests.get(pdf_url)
    if response.status_code != 200:
        raise Exception(f"❌ Failed to download PDF: Status code {response.status_code}")

    print(f"🚀 Uploading to s3://{s3_bucket}/{s3_key}")
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=s3_bucket,
        Key=s3_key,
        Body=response.content,
        ContentType="application/pdf"
    )

    print(f"✅ Upload complete: s3://{s3_bucket}/{s3_key}")
    return {
        "statusCode": 200,
        "message": "Bulletin downloaded and uploaded to S3.",
        "s3_key": s3_key,
        "source_url": pdf_url
    }
