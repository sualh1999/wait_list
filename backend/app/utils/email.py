from sib_api_v3_sdk import ApiClient, Configuration, TransactionalEmailsApi, SendSmtpEmail
import logging
from ..config import settings

logger = logging.getLogger(__name__)

async def send_welcome_email(to_email: str):
    if not settings.API_KEY or not settings.SENDER_EMAIL:
        logger.warning("API_KEY or SENDER_EMAIL is not set. Skipping email sending.")
        return

    # Configure API key authorization: api-key
    configuration = Configuration()
    configuration.api_key['api-key'] = settings.API_KEY

    # Create an API client
    api_client = ApiClient(configuration)
    api_instance = TransactionalEmailsApi(api_client)

    subject = "Welcome to the Waitlist!"

    # HTML version of the email
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to the Waitlist!</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
            .container {{ max-width: 600px; margin: 20px auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); }}
            .header {{ text-align: center; padding-bottom: 20px; border-bottom: 1px solid #eeeeee; }}
            .header h1 {{ color: #333333; font-size: 28px; margin: 0; }}
            .content {{ padding: 20px 0; line-height: 1.6; color: #555555; font-size: 16px; }}
            .content p {{ margin-bottom: 15px; }}
            .footer {{ text-align: center; padding-top: 20px; margin-top: 30px; border-top: 1px solid #eeeeee; font-size: 12px; color: #aaaaaa; }}
            .footer p {{ margin: 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Welcome to Our Waitlist!</h1>
            </div>
            <div class="content">
                <p>Hi there,</p>
                <p>Thank you for joining our waitlist! We're excited to have you.</p>
                <p>You'll be among the first to know when we have exciting updates to share.</p>
                <p>Stay tuned!</p>
            </div>
            <div class="footer">
                <p>&copy; 2025 Waitlist App. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    send_smtp_email = SendSmtpEmail(
        sender={"name": "Waitlist App", "email": settings.SENDER_EMAIL},
        to=[{"email": to_email}],
        subject=subject,
        html_content=html_content
    )

    logger.info(f"Attempting to send email to {to_email} using Brevo...")
    try:
        response = api_instance.send_transac_email(send_smtp_email)
        logger.info(f"Email sent successfully to {to_email}: {response}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}", exc_info=True)