import httpx
from ..config import settings

async def send_welcome_email(to_email: str):
    if not settings.RESEND_API_KEY:
        print("RESEND_API_KEY is not set. Skipping email sending.")
        return

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to the Waitlist!</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}\n            .container {{ max-width: 600px; margin: 20px auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); }}\n            .header {{ text-align: center; padding-bottom: 20px; border-bottom: 1px solid #eeeeee; }}\n            .header h1 {{ color: #333333; font-size: 28px; margin: 0; }}\n            .content {{ padding: 20px 0; line-height: 1.6; color: #555555; font-size: 16px; }}\n            .content p {{ margin-bottom: 15px; }}\n            .button-container {{ text-align: center; margin-top: 20px; }}\n            .button {{ display: inline-block; padding: 12px 25px; background-color: #007bff; color: #ffffff; text-decoration: none; border-radius: 5px; font-size: 16px; font-weight: bold; }}\n            .footer {{ text-align: center; padding-top: 20px; margin-top: 30px; border-top: 1px solid #eeeeee; font-size: 12px; color: #aaaaaa; }}\n            .footer p {{ margin: 0; }}\n        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Welcome to Our Waitlist!</h1>
            </div>
            <div class="content">
                <p>Hi there,</p>
                <p>Thank you for showing interest in our upcoming product! We're thrilled to have you on board.</p>
                <p>You've successfully joined our exclusive waitlist. We'll be working hard to bring you an amazing experience, and you'll be among the first to know when we launch.</p>
                <p>Stay tuned for updates!</p>
                <div class="button-container">
                    <a href="#" class="button">Visit Our Website</a>
                </div>
            </div>
            <div class="footer">
                <p>&copy; 2025 Waitlist App. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    headers = {
        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "from": "Waitlist App <onboarding@resend.dev>", # Replace with your verified Resend domain
        "to": [to_email],
        "subject": "Welcome to the Waitlist!",
        "html": html_content
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("https://api.resend.com/emails", headers=headers, json=data)
            response.raise_for_status()
            print(f"Email sent successfully to {to_email}: {response.json()}")
        except httpx.HTTPStatusError as e:
            print(f"Failed to send email to {to_email}: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"An error occurred while sending email to {to_email}: {e}")
