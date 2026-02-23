import smtplib
from email.mime.text import MIMEText

EMAIL_FROM = "mat@gmail.com"
EMAIL_PASS = "uhphssivvrxorojr"
EMAIL_TO = "mat@gmail.com"

def send_alert(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_FROM, EMAIL_PASS)
    server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    server.quit()
