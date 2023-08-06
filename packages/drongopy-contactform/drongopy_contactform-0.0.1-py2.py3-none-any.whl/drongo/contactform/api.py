from drongo.utils.endpoint import APIEndpoint
from drongo.utils.helpers import URLHelper


class ContactFormSubmit(APIEndpoint):
    __url__ = '/contact-form/{instance}/submit'
    __http_methods__ = ['POST']

    def init(self):
        self.cf_svc = self.ctx.modules.contactform.services
        self.obj = self.ctx.request.json

    def call(self):
        svc = self.cf_svc.ContactFormSubmit(body=self.obj)
        svc.call(ns=self.ns, instance=self.instance)
        return 'OK'


AVAILABLE_API = [
    ContactFormSubmit
]


class ContactFormAPI(object):
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
