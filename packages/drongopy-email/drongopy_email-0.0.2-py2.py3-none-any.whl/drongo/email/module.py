import logging

from drongo.addons.database import Database
from drongo.module import Module


class Email(Module):
    """Drongo module for sending emails."""

    __default_config__ = {
        'api_base_url': '',

        'backend': 'smtp',
        'namespace_service': 'http://ns:8000'
    }

    logger = logging.getLogger('email')

    def init(self, config):
        self.logger.info('Initializing [email] module.')

        self.app.context.modules.email = self

        if config.backend == 'smtp':
            from .backends import _smtp
            services = self.services = _smtp

        else:
            raise NotImplementedError

        services.EmailServiceBase.init(module=self)

        self.init_api()

    def init_api(self):
        from .api import EmailAPI
        self.api = EmailAPI(
            app=self.app,
            module=self,
            base_url=self.config.api_base_url + '/{ns}'
        )
