import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


# def send_verification_email(to_email: str, code: str):
#     subject = "GeniStudy - Tasdiqlash kodi"
#     body = f"Sizning tasdiqlash kodingiz: {code}"

#     em = EmailMessage()
#     em["From"] = SMTP_EMAIL
#     em["To"] = to_email
#     em["Subject"] = subject
#     em.set_content(body)

#     context = ssl.create_default_context()

#     with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
#         smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
#         smtp.send_message(em)
    



def send_verification_email(to_email: str, code: str):
    subject = "GeniStudy - Tasdiqlash kodi"
    
    # Oddiy matn (fallback)
    text_content = f"Sizning tasdiqlash kodingiz: {code}"

    # HTML shaklida matn
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                <h2 style="color: #333;">GeniStudy - Tasdiqlash kodi</h2>
                <p style="font-size: 16px; color: #555;">Quyidagi kodni saytimizda kiriting:</p>
                <p style="font-size: 24px; font-weight: bold; color: #2c7be5; text-align: center;">{code}</p>
                <hr>
                <p style="font-size: 14px; color: #999;">Agar bu xabar sizga noto‘g‘ri yuborilgan bo‘lsa, iltimos, e'tibor bermang.</p>
            </div>
        </body>
    </html>
    """

    em = EmailMessage()
    em["From"] = SMTP_EMAIL
    em["To"] = to_email
    em["Subject"] = subject
    em.set_content(text_content)
    em.add_alternative(html_content, subtype="html")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
        smtp.send_message(em)
