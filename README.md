🕊️ Church Bulletin Summarization Automation

This project automates the weekly summarization of the St. John the Baptist church bulletin. It downloads the latest bulletin PDF, summarizes it using a tailored prompt with OpenAI, and sends the results (including a link to the PDF) via email. This helps parishioners quickly understand the week's events, volunteer opportunities, and sermon themes without reading the full bulletin.
🏗️ Architecture Overview

This automation is composed of three AWS Lambda functions, orchestrated by an AWS Step Function that runs on a configurable schedule (e.g., Sundays at 10am).
Workflow

    download_bulletin Lambda – Downloads the weekly bulletin PDF from a URL based on the current date and uploads it to S3.

    summarize_bulletin Lambda – Downloads the PDF from S3, extracts text, and summarizes it using a structured OpenAI prompt.

    delete_bulletins Lambda – Cleans up the S3 bucket by deleting processed bulletin PDFs.

Each function is packaged and deployed independently as a zipped Lambda artifact.
📦 Lambda Function Descriptions
download_bulletin

    Constructs the URL for the current week's bulletin.

    Downloads the PDF file.

    Uploads it to a configured S3 bucket with a timestamp-based key.

summarize_bulletin

    Downloads the bulletin PDF from S3.

    Uses OCR or PDF text extraction to read the contents.

    Sends the content to OpenAI with a prompt that summarizes the bulletin into:

        Upcoming Events

        Volunteer Opportunities

        Sermon Topics

        Organization Spotlights

    Sends the summary and bulletin link via email (SMTP or AWS SES).

delete_bulletins

    Deletes bulletin PDFs from the S3 bucket after processing is complete to avoid storage clutter.

🔄 Updating Lambda Code

To update the code for any of the Lambda functions, follow these steps:
1. Modify Code

Update the Python source code (lambda_function.py) or dependencies (requirements.txt) in the appropriate directory:

    summarize_bulletin/

    download_bulletin/

    delete_bulletins/

2. Run Build Script

Use build_lambda_zip.sh to create the zip file

3. Grab the required zip and update the Lambda