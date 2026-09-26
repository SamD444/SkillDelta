import os
import requests


MAILJET_API_KEY = os.getenv("MJ_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MJ_SECRET_KEY")
FROM_EMAIL = os.getenv("EMAIL_ADDRESS")


def send_email(
    to_email: str,
    subject: str,
    html_body: str,
    text_body: str = None
) -> bool:

    try:
        if not MAILJET_API_KEY:
            print("Mailjet API key missing.")
            return False

        if not MAILJET_SECRET_KEY:
            print("Mailjet Secret Key missing.")
            return False

        if not FROM_EMAIL:
            print("Email sender address missing.")
            return False

        url = "https://api.mailjet.com/v3.1/send"

        email_data = {
            "Messages": [
                {
                    "From": {
                        "Email": FROM_EMAIL,
                        "Name": "SkillDelta"
                    },
                    "To": [
                        {
                            "Email": to_email
                        }
                    ],
                    "Subject": subject,
                    "HTMLPart": html_body
                }
            ]
        }

        if text_body:
            email_data["Messages"][0]["TextPart"] = text_body

        response = requests.post(
            url,
            auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY),
            json=email_data,
            timeout=20
        )

        if response.status_code in (200, 201):
            print("SkillDelta Email sent via Mailjet.")
            return True

        print("Mailjet Error:", response.text)
        return False

    except Exception as e:
        print("Mailjet Email Error:", str(e))
        return False