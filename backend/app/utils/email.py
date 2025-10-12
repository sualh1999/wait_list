import httpx
from ..config import settings

async def send_welcome_email(to_email: str):
    if not settings.RESEND_API_KEY:
        print("RESEND_API_KEY is not set. Skipping email sending.")
        return

    headers = {
        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "from": "Waitlist App <onboarding@resend.dev>", # Replace with your verified Resend domain
        "to": [to_email],
        "subject": "Welcome to the Waitlist!",
        "html": "<strong>Thank you for joining our waitlist!</strong> We'll notify you when we launch."
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
