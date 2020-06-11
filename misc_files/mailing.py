import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_verify_link(to_address, username, link):
    msg = MIMEMultipart()
    msg['From'] = 'Creative Spaces'
    msg['To'] = to_address
    msg['Subject'] = 'Verify Link'

    body = 'Hello {}, Your verification link is {}'.format(username, link)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('creativespacesbyhvirdi@gmail.com', 'Creative@123')
    text = msg.as_string()
    server.sendmail('creativespacesbyhvirdi@gmail.com', to_address, text)
    server.quit()
