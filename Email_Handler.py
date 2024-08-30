import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email_Handler:
    def __init__(self, email, password, smtp_server, smtp_port, imap_server, imap_port):
        self.email = email
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.imap_server = imap_server
        self.imap_port = imap_port

    def send_email(self, to, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"发送邮件时出错: {e}")
            return False

    def receive_emails(self, folder='INBOX', limit=10):
        try:
            with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as server:
                server.login(self.email, self.password)
                server.select(folder)
                _, message_numbers = server.search(None, 'ALL')
                
                emails = []
                for num in message_numbers[0].split()[-limit:]:
                    _, msg = server.fetch(num, '(RFC822)')
                    email_body = msg[0][1]
                    email_message = email.message_from_bytes(email_body)
                    
                    subject = email_message['Subject']
                    sender = email.utils.parseaddr(email_message['From'])[1]
                    
                    if email_message.is_multipart():
                        content = ''
                        for part in email_message.get_payload():
                            if part.get_content_type() == 'text/plain':
                                content += part.get_payload(decode=True).decode()
                    else:
                        content = email_message.get_payload(decode=True).decode()
                    
                    emails.append({
                        'subject': subject,
                        'sender': sender,
                        'content': content
                    })
                
                return emails[::-1]  # 返回最新的邮件在前
        except Exception as e:
            print(f"接收邮件时出错: {e}")
            return []