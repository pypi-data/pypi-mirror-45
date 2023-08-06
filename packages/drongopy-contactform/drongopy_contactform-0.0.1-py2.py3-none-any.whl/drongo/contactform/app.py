import logging
import os

from drongo.addons.database import Database
from drongo.app import Drongo
from drongo.contactform.module import ContactForm

LOGGING_FORMAT = (
    '\033[36m%(asctime)-24s \033[34m%(name)-16s '
    '\033[32m%(levelname)-8s \033[97m%(message)s\033[39m'
)
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)


app = Drongo()

ContactForm(app)
