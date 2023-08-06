import smtplib
import logging
from drongo_client.ns import NSClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailServiceBase(object):
    DEFAULT_SETTINGS = {}

    @classmethod
    def init(cls, module):
        cls.module = module
        cls._ns_client = NSClient(module.config.namespace_service)

    def get_settings(self, ns='core', instance=None):
        self._ns_client.set_namespace(ns)
        _, settings = self._ns_client.ns_modules_get_settings(
            'email', instance)
        logging.warn(settings)

        self.settings = {}
        self.settings.update(self.DEFAULT_SETTINGS)
        self.settings.update(settings or {})

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass


class SendEmailService(EmailServiceBase):
    def __init__(self, email_from, email_to, subject, email_cc=[], email_bcc=[], message_text=None, message_html=None, attachments=[]):
        self.email_from = email_from
        self.email_to = email_to
        self.subject = subject
        self.email_cc = email_cc
        self.email_bcc = email_bcc
        self.message_text = message_text
        self.message_html = message_html
        self.attachments = attachments

    def _connect(self):
        self._smtp = smtplib.SMTP(
            host=self.settings.get('smtp_host'),
            port=self.settings.get('smtp_port'))
        self._smtp.starttls()
        self._smtp.login(
            self.settings.get('smtp_user'),
            self.settings.get('smtp_password'))

    def _send(self):
        msg = MIMEMultipart()
        if self.message_text is not None:
            msg.attach(MIMEText(self.message_text, 'plain'))

        if self.message_html is not None:
            msg.attach(MIMEText(self.message_html, 'html'))

        msg['From'] = self.email_from
        msg['To'] = ', '.join(self.email_to)
        msg['Subject'] = self.subject

        self._smtp.send_message(msg)
        # TODO: Implement cc, bcc and attachments

    def _disconnect(self):
        self._smtp.close()

    def call(self, ns='core', instance=None):
        self.get_settings(ns=ns, instance=instance)
        self._connect()
        self._send()
        self._disconnect()
