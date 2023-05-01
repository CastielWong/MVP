#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This tool is used for mailing."""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass
from typing import List
from smtplib import SMTPAuthenticationError
import smtplib
import ssl

from typing_extensions import TypedDict

Server = TypedDict("Server", {"host": str, "port": int})

SMTP_SERVER = {
    "host": "smtp.gmail.com",
    "port": 465,
}  # type: Server


# pylint: disable=R1711 (useless-return)
def send_out_corporate(
    smtp_server: str, sender: str, receiver: str, subject: str, body: str
) -> None:
    """Send out email via corporate SMTP server.

    Args:
        smtp_server: SMTP server the corporate set up, e.g, "smtp-au.xxx.com"
        sender: the address used to send emails, e.g, "product_control@xxx.com"
        receiver: address to receive the email
        subject: email title
        body: content of the email
    """
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))
    print(msg.as_string())

    with smtplib.SMTP(smtp_server) as server:
        server.sendmail(from_addr=sender, to_addrs=receiver, msg=msg.as_string())

    return


# pylint: disable=R0913 (too-many-arguments)
def send_out_personal(
    sender: str,
    password: str,
    receiver: str,
    subject: str,
    body: str,
    copy_list: List[str] = None,
) -> bool:
    """Send out email via third-party SMTP server.

    Args:
        sender: the address used to send emails, e.g, "xxx@gmail.com"
        password: password to the personal email
        receiver: address to receive the email
        subject: email title
        body: content of the email
        copy_list: emails to copy to

    Returns:
        True if email is sent successfully.
    """
    msg = MIMEMultipart()

    # config meta needed
    msg["From"] = sender

    # it doesn't matter what's in "To", "Cc" or "Bcc"
    # only those addresses set when send matters
    msg["To"] = receiver
    others = ""
    if copy_list is not None:
        others = ", ".join(copy_list)
        msg["Cc"] = others
    # msg["Bcc"] = ""

    msg["Subject"] = subject

    part_1 = MIMEText(body, "plain")
    part_2 = MIMEText(body, "html")

    msg.attach(part_1)
    msg.attach(part_2)

    print(msg)

    try:
        context = ssl.create_default_context()

        # need to enable "Less secure app access" on Gmail account first
        with smtplib.SMTP_SSL(
            SMTP_SERVER["host"], SMTP_SERVER["port"], context=context
        ) as server:
            server.login(sender, password)
            # email will be only sent to the ones actually needed
            recipients = f"{receiver}, {others}"

            # note: it failed to send emails to cc, though the email list can be seen
            server.sendmail(from_addr=sender, to_addrs=recipients, msg=msg.as_string())
            # server.send_message(msg=msg, from_addr=sender, to_addrs=emails)
    except SMTPAuthenticationError as ex:
        print("Fail to send out the email, below is the exception encountered:")
        print(ex)
        return False

    print("Email is sent out successfully.")

    return True


# pylint: disable=C0103 (invalid-name)
if __name__ == "__main__":
    email_sender = "caswexp@gmail.com"
    # note `getpass` works in terminal
    pwd = getpass(prompt="Input password: ")
    email_receiver = "caswexp@gmail.com"
    email_title = "testing"
    content = """\
        Hello mail

        testing
    """

    send_out_personal(
        sender=email_sender,
        password=pwd,
        receiver=email_receiver,
        subject=email_title,
        body=content,
        # copy_list=[]
    )
