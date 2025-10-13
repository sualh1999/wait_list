import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import asyncio # Import asyncio
from ..config import settings

logger = logging.getLogger(__name__)

def _send_sync_email(to_email: str, msg: MIMEMultipart):
    """Synchronous helper function to send email."""
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
            server.starttls()
            server.login(settings.GMAIL_USER, settings.GMAIL_PASS)
            server.send_message(msg)
        logger.info(f"Email sent successfully to {to_email}")
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication Error: Failed to log in to SMTP server. Check GMAIL_USER and GMAIL_PASS. Error: {e}")
        raise # Re-raise to be caught by the async function
    except smtplib.SMTPServerDisconnected as e:
        logger.error(f"SMTP Server Disconnected: The SMTP server unexpectedly disconnected. Error: {e}")
        raise
    except smtplib.SMTPConnectError as e:
        logger.error(f"SMTP Connect Error: Failed to connect to the SMTP server. Check host and port. Error: {e}")
        raise
    except smtplib.SMTPException as e:
        logger.error(f"SMTP Error: An unexpected SMTP error occurred. Error: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred while sending email to {to_email}: {e}", exc_info=True)
        raise


async def send_welcome_email(to_email: str):
    if not settings.GMAIL_USER or not settings.GMAIL_PASS:
        logger.warning("GMAIL_USER or GMAIL_PASS is not set. Skipping email sending.")
        return

    subject = "Welcome to the Waitlist!"

    # Plain text version of the email
    plain_text_content = (
        "Thank you for joining our waitlist! We're excited to have you.\n\n"
        "You'll be among the first to know when we have exciting updates to share.\n\n"
        "Stay tuned!\n\n"
        "\n© 2025 Waitlist App. All rights reserved."
    )

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

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.GMAIL_USER
    msg["To"] = to_email

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML part, is best and preferred.
    msg.attach(MIMEText(plain_text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    logger.info(f"Attempting to send email to {to_email}...")
    logger.debug(f"Email message details: From={msg['From']}, To={msg['To']}, Subject={msg['Subject']}")
    try:
        await asyncio.to_thread(_send_sync_email, to_email, msg)
    except Exception: # Catch exceptions re-raised from _send_sync_email
        logger.error(f"Failed to send email to {to_email} after retries.")
