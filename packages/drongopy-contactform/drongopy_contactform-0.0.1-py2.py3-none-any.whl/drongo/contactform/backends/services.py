import smtplib
from drongo_client.ns import NSClient
from drongo_client.email import EmailClient

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template


class CFServiceBase(object):
    DEFAULT_SETTINGS = {}

    @classmethod
    def init(cls, module):
        cls.module = module
        cls._ns_client = NSClient(module.config.namespace_service)
        cls._email_client = EmailClient(module.config.email_service)

    def get_settings(self, ns='core', instance=None):
        self._ns_client.set_namespace(ns)
        _, settings = self._ns_client.ns_modules_get_settings(
            'contact-form', instance)

        self.settings = {}
        self.settings.update(self.DEFAULT_SETTINGS)
        self.settings.update(settings or {})

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass


class ContactFormSubmit(CFServiceBase):
    def __init__(self, body):
        self.body = body

    def call(self, ns='core', instance=None):
        self.get_settings(ns, instance)
        self._email_client.set_namespace(ns)
        self._email_client.set_instance(self.settings.get('email_instance'))
        self._email_client.send_email(
            email_from=self.settings.get('email_from'),
            email_to=self.settings.get('email_to', '').split(','),
            subject=Template(self.settings.get('subject')).render(self.body),
            message_html=Template(
                self.settings.get('message_template')).render(self.body)
        )
