import boto3
import smtplib
from email.mime.text import MIMEText
import openai
import json

def get_secret(secret_name):
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

def get_openai_response(prompt, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
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

def lambda_handler(event, context):
    # Load secrets
    secret = get_secret("church-bulletin-bot/credentials")
    openai_key = secret["openai_api_key"]
    gmail_user = secret["gmail_address"]
    gmail_pass = secret["gmail_app_password"]

    # Ask OpenAI the question
    prompt = "What is Wrexham football?"
    answer = get_openai_response(prompt, openai_key)

    # Send email
    recipient = "joe.mcconnell10@gmail.com"  # <<< Put your email here
    send_email_via_gmail(
        subject="OpenAI Response: Wrexham Football",
        body=answer,
        sender_email=gmail_user,
        app_password=gmail_pass,
        recipient_email=recipient
    )

    return {
        "statusCode": 200,
        "message": "OpenAI response sent via email.",
        "preview": answer[:200]
    }
