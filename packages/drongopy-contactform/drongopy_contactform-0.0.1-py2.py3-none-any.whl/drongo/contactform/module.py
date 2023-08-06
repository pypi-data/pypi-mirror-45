import logging

from drongo.addons.database import Database
from drongo.module import Module


class ContactForm(Module):
    """Drongo module for handling contact forms."""

    __default_config__ = {
        'api_base_url': '',

        'namespace_service': 'http://ns:8000',
        'email_service': 'http://email:8000'
    }

    logger = logging.getLogger('contactform')

    def init(self, config):
        self.logger.info('Initializing [contactform] module.')

        self.app.context.modules.contactform = self

        from .backends import services
        self.services = services

        services.CFServiceBase.init(module=self)

        self.init_api()

    def init_api(self):
        from .api import ContactFormAPI
        self.api = ContactFormAPI(
            app=self.app,
            module=self,
            base_url=self.config.api_base_url + '/{ns}'
        )
