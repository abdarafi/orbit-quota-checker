import smtplib, datetime

smtp_user = 'example'
smtp_password = 'examplepassword'

sent_from = "Example <example@example.com>"
to = ['example_recipient@example.com']
subject = '[UPDATES] Daily Internet Quota - {}'.format(datetime.datetime.now().date())
body = "Body"

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)
try:
    server = smtplib.SMTP('mail.smtp.com', 2525)
    server.login(smtp_user, smtp_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print('Email sent!')
except Exception as e:
    print('Something went wrong with sending email: {}'.format(str(e)))
