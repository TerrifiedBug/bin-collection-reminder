"""Notification services for bin collection reminders."""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict

import requests


def send_discord_notification(webhook_url: str, message: str) -> bool:
    """Send a message to a Discord webhook.

    Args:
        webhook_url: The Discord webhook URL
        message: The message to send

    Returns:
        bool: True if notification was sent successfully
    """
    try:
        response = requests.post(
            webhook_url,
            json={"content": message, "username": "Bin Collection Reminder"},
            timeout=10,
        )
        response.raise_for_status()
        print("[🔔] Discord notification sent.")
        return True
    except requests.RequestException as error:
        print(f"[!] Discord notification failed: {error}")
        return False


def send_whatsapp_notification(phone_number: str, api_key: str, message: str) -> bool:
    """Send a message via CallMeBot WhatsApp API.

    Args:
        phone_number: The phone number to send to
        api_key: CallMeBot API key
        message: The message to send

    Returns:
        bool: True if notification was sent successfully
    """
    try:
        url = (
            f"https://api.callmebot.com/whatsapp.php?"
            f"phone={phone_number}&apikey={api_key}&text={requests.utils.quote(message)}"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print("[📱] WhatsApp notification sent.")
        return True
    except requests.RequestException as error:
        print(f"[!] WhatsApp notification failed: {error}")
        return False


def send_email_notification(
    smtp_server: str,
    smtp_port: int,
    sender_email: str,
    sender_password: str,
    recipient_email: str,
    message: str,
    subject: str = "Bin Collection Reminder",
) -> bool:
    """Send an email notification using SMTP.

    Args:
        smtp_server: The SMTP server address (e.g., smtp.gmail.com)
        smtp_port: The SMTP port (e.g., 587 for TLS)
        sender_email: The sender's email address
        sender_password: The sender's email password or app password
        recipient_email: The recipient's email address
        message: The message to send
        subject: The email subject line

    Returns:
        bool: True if email was sent successfully
    """
    try:
        # Create message container
        email_message = MIMEMultipart()
        email_message["From"] = sender_email
        email_message["To"] = recipient_email
        email_message["Subject"] = subject

        # Attach the message
        email_message.attach(MIMEText(message, "plain"))

        # Connect to server and send
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(email_message)

        print("[📧] Email notification sent.")
        return True
    except Exception as error:
        print(f"[!] Email notification failed: {error}")
        return False


def send_notifications(collection: Dict[str, str]) -> None:
    """Send notifications based on environment config.

    Args:
        collection: Dictionary containing bin collection information
    """
    message = f"Reminder: {collection['day']} - {collection['type']}"

    # Discord notifications
    if os.getenv("DISCORD_ENABLED", "false").lower() == "true":
        webhook_url = os.getenv("DISCORD_WEBHOOK")
        if webhook_url:
            send_discord_notification(webhook_url, message)
        else:
            print("[!] Discord enabled but no webhook URL provided.")

    # WhatsApp notifications via CallMeBot
    if os.getenv("WHATSAPP_ENABLED", "false").lower() == "true":
        phone_number = os.getenv("WHATSAPP_PHONE")
        api_key = os.getenv("WHATSAPP_APIKEY")

        if phone_number and api_key:
            send_whatsapp_notification(phone_number, api_key, message)
        else:
            print("[!] WhatsApp enabled but missing phone number or API key.")

    # Email notifications
    if os.getenv("EMAIL_ENABLED", "false").lower() == "true":
        smtp_server = os.getenv("EMAIL_SMTP_SERVER")
        smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587"))
        sender_email = os.getenv("EMAIL_SENDER")
        sender_password = os.getenv("EMAIL_PASSWORD")
        recipient_email = os.getenv("EMAIL_RECIPIENT")

        if all([smtp_server, sender_email, sender_password, recipient_email]):
            send_email_notification(
                smtp_server,
                smtp_port,
                sender_email,
                sender_password,
                recipient_email,
                message,
            )
        else:
            print("[!] Email enabled but missing one or more required settings.")
