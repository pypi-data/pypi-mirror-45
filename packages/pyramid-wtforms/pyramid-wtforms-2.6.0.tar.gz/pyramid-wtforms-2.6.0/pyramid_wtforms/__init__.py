from wtforms import widgets
from wtforms.validators import ValidationError
import pkg_resources

from . import validators
from .fields import *
from .forms import Form, SecureForm


__version__ = pkg_resources.get_distribution('pyramid_wtforms').version
