from drongo.utils.endpoint import APIEndpoint
from drongo.utils.helpers import URLHelper


# TODO: Implement email queueing

class EmailSend(APIEndpoint):
    __url__ = '/email/{instance}/send'
    __http_methods__ = ['POST']

    def init(self):
        self.email_svc = self.ctx.modules.email.services
        self.obj = self.ctx.request.json

    def call(self):
        # TODO: Implement cc, bcc and attachments
        svc = self.email_svc.SendEmailService(
            email_from=self.obj.get('email_from'),
            email_to=self.obj.get('email_to'),
            subject=self.obj.get('subject'),
            message_text=self.obj.get('message_text'),
            message_html=self.obj.get('message_html')
        )
        svc.call()
        return 'OK'


AVAILABLE_API = [
    EmailSend
]


class EmailAPI(object):
    def __init__(self, app, module, base_url):
        self.app = app
        self.module = module
        self.base_url = base_url

        self.init_endpoints()

    def init_endpoints(self):
        for endpoint in AVAILABLE_API:
            URLHelper.endpoint(
                app=self.app,
                klass=endpoint,
                base_url=self.base_url
            )
