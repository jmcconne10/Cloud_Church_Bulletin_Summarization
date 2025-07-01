import boto3
import smtplib
from email.mime.text import MIMEText
import openai
import json
import time

# === Configuration ===
S3_BUCKET = "church-bulletin-bot"
S3_KEY = "bulletin_20250629.pdf"
SECRET_NAME = "church-bulletin-bot/credentials"


# === Helpers ===
def get_secret(secret_name):
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])


def extract_text_from_textract(bucket, key):
    textract = boto3.client("textract")

    start_response = textract.start_document_text_detection(
        DocumentLocation={'S3Object': {'Bucket': bucket, 'Name': key}}
    )
    job_id = start_response['JobId']

    # Poll until complete
    while True:
        response = textract.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]
        if status in ["SUCCEEDED", "FAILED"]:
            break
        time.sleep(5)

    if status == "FAILED":
        raise Exception("Textract job failed")

    # Gather all text lines
    lines = []
    next_token = None
    while True:
        if next_token:
            response = textract.get_document_text_detection(JobId=job_id, NextToken=next_token)
        else:
            response = textract.get_document_text_detection(JobId=job_id)

        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                lines.append(block['Text'])

        next_token = response.get('NextToken')
        if not next_token:
            break

    return "\n".join(lines)


def get_openai_response(prompt, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",  # Updated model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']


def send_email_via_gmail(subject, body, sender_email, app_password, recipient_email):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)


# === Lambda Entry Point ===
def lambda_handler(event, context):
    # Load secrets
    secret = get_secret(SECRET_NAME)
    openai_key = secret["openai_api_key"]
    gmail_user = secret["gmail_address"]
    gmail_pass = secret["gmail_app_password"]
    recipient_address = secret["recipient_address"]

    # Extract text from bulletin PDF
    bulletin_text = extract_text_from_textract(S3_BUCKET, S3_KEY)

    # Summarize events using OpenAI
    openai_prompt = f"Read this church bulletin and summarize only the upcoming events for this week:\n\n{bulletin_text}"
    summary = get_openai_response(openai_prompt, openai_key)

    # Email the summary
    send_email_via_gmail(
        subject="Church Bulletin Events Summary",
        body=summary,
        sender_email=gmail_user,
        app_password=gmail_pass,
        recipient_email=recipient_address
    )

    return {
        "statusCode": 200,
        "message": "Bulletin summary emailed.",
        "preview": summary[:300]
    }
