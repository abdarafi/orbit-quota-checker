import smtplib
import datetime
import os


def send(message: str):

    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    DEST_EMAIL = os.getenv("DEST_EMAIL")
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_ADDRESS = os.getenv("SMTP_ADDRESS")
    SMTP_PORT = int(os.getenv("SMTP_PORT"))

    smtp_user = SMTP_USER
    smtp_password = SMTP_PASSWORD

    sent_from = SENDER_EMAIL
    to = [DEST_EMAIL]
    subject = '[UPDATES] Daily Internet Quota - {}'.format(
        datetime.datetime.now().date())
    body = message

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP(SMTP_ADDRESS, SMTP_PORT)
        server.login(smtp_user, smtp_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except Exception as e:
        print('Something went wrong with sending email: {}'.format(str(e)))
