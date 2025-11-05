import smtplib
from email.message import EmailMessage
from pathlib import Path
from datetime import datetime

def send_email(sender_email: str, sender_password: str, receiver_email: str, subject: str, message: str, str_path: str) -> None:
    """

    :rtype: object
    """
    # --- Create the email ---
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(message)

    # --- Add attachment ---
    attachment_path = Path(str_path)
    with open(attachment_path, "rb") as f:
        msg.add_attachment(f.read(),
                           maintype="image",
                           subtype="jpeg",
                           filename=attachment_path.name)

    # --- Send the email (Gmail example) ---
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

    print(f" Email sent on the {datetime.now().strftime('%d/%m/%y at %H:%M')} from {sender_email} to {receiver_email}!")

