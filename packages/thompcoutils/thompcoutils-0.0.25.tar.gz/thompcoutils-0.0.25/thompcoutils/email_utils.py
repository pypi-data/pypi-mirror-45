import smtplib
import os
from email import encoders
import mimetypes
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from thompcoutils.config_utils import ConfigManager
from thompcoutils.log_utils import get_logger

if os.name == 'nt' or os.name == "posix":
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
else:
    # noinspection PyUnresolvedReferences
    from email.MIMEMultipart import MIMEMultipart
    # noinspection PyUnresolvedReferences
    from email.MIMEText import MIMEText
    # noinspection PyUnresolvedReferences
    from email.MIMEApplication import MIMEApplication


class EmailConnection:
    TITLE = "email connection"
    USERNAME = "username"
    PASSWORD = "password"
    FROM = "from"
    SMTP = "smtp"
    PORT = "port"

    def __init__(self, cfg_mgr=None, username=None, password=None, from_user=None, smtp=None, port=None):
        if cfg_mgr is None:
            self.username = username
            self.password = password
            self.from_user = from_user
            self.smtp = smtp
            self.port = port
        else:
            self.username = cfg_mgr.read_entry(EmailConnection.TITLE, EmailConnection.USERNAME,
                                               "myname@google.com", str)
            self.password = cfg_mgr.read_entry(EmailConnection.TITLE, EmailConnection.PASSWORD,
                                               "mySecretPassword", str)
            self.from_user = cfg_mgr.read_entry(EmailConnection.TITLE, EmailConnection.FROM,
                                                "Email Sender", str)
            self.smtp = cfg_mgr.read_entry(EmailConnection.SMTP, EmailConnection.FROM,
                                           "smtp.gmail.com", str)
            self.port = cfg_mgr.read_entry(EmailConnection.PORT, EmailConnection.FROM,
                                           587, int)


class EmailSender:
    def __init__(self, email_connection):
        self.email_connection = email_connection

    def send(self, to_email, subject, message, attach_files=None):
        logger = get_logger()
        server = None
        try:
            server = smtplib.SMTP(self.email_connection.smtp, self.email_connection.port)
            server.ehlo()
            server.starttls()
            server.login(self.email_connection.username, self.email_connection.password)
            outer_msg = MIMEMultipart('alternative')
            sender = self.email_connection.from_user
            recipients = to_email
            outer_msg['Subject'] = subject
            outer_msg.attach(MIMEText(message, "html"))
            outer_msg['From'] = self.email_connection.from_user
            if isinstance(recipients, list):
                outer_msg['To'] = ", ".join(recipients)
            else:
                outer_msg['To'] = recipients
            if attach_files is not None:
                for filename in attach_files:
                    file_type, encoding = mimetypes.guess_type(filename)
                    if file_type is None or encoding is not None:
                        file_type = 'application/octet-stream'
                    maintype, subtype = file_type.split('/', 1)
                    if maintype == 'text':
                        with open(filename) as fp:
                            msg = MIMEText(fp.read(), _subtype=subtype)
                    elif maintype == 'image':
                        with open(filename, 'rb') as fp:
                            msg = MIMEImage(fp.read(), _subtype=subtype)
                    elif maintype == 'audio':
                        with open(filename, 'rb') as fp:
                            msg = MIMEAudio(fp.read(), _subtype=subtype)
                    else:
                        with open(filename, 'rb') as fp:
                            msg = MIMEBase(maintype, subtype)
                            msg.set_payload(fp.read())
                        encoders.encode_base64(msg)
                    msg.add_header('Content-Disposition', 'attachment', filename=filename)
                    outer_msg.attach(msg)
            server.sendmail(sender, recipients, outer_msg.as_string())
            logger.debug("Successfully sent mail to " + str(recipients))
        except Exception as e:
            logger.warning("Failed to send mail to {} because {}".format(to_email, str(e)))
        finally:
            if server is not None:
                server.quit()


def main():
    send_file = True
    use_parameters = False
    if use_parameters:
        mail = EmailSender(EmailConnection(username="jorythompson@gmail.com",
                                           password="warfzdvvcovseosv",
                                           from_user="Test",
                                           smtp="smtp.gmail.com",
                                           port=587))
        subject = "using parameters"
    else:
        config = ConfigManager("email.ini")
        mail = EmailSender(EmailConnection(config))
        subject = "using configuration file"

    if send_file:
        mail.send(to_email="Jordan@ThompCo.com", subject="this is a test from emailSender",
                  message="Here is the message using parameters passed in with an attached file",
                  attach_files=[os.path.basename(__file__)])
    else:
        mail.send("jorythompson@gmail.com", "this is a test from emailSender {}".format(subject),
                  "This is a test message")


if __name__ == "__main__":
    main()
