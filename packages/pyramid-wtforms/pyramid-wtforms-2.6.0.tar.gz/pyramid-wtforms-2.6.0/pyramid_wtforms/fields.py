from cgi import FieldStorage as _CGIFieldStorage

from wtforms.fields import *
from wtforms.widgets import (ListWidget as _ListWidget,
                             CheckboxInput as _CheckboxInput)

from .widgets import MultipleFilesInput as _MultipleFilesInput
from .storage import FieldStorage as _FieldStorage


_FileField = FileField


class FileField(_FileField):
    """Used for handling single file field."""

    def process_formdata(self, valuelist):
        if len(valuelist) != 1:
            raise ValueError(self.gettext('Only accept one file '
                                          'if the field is present.'))
        # valuelist will be [b''] if no file uploaded, set data to None
        if valuelist == [b'']:
            self.data = None
        # valuelist will be [] if the post field is not provided as file
        # raise error since it could be malicious access
        elif valuelist == []:
            raise ValueError(self.gettext('Only accept a file.'))
        else:
            if isinstance(valuelist[0], _FieldStorage):
                self.data = valuelist[0]
            else:
                self.data = _FieldStorage(valuelist[0])


class MultipleFilesField(_FileField):
    """Used for handling multi files field."""

    widget = _MultipleFilesInput()

    def process_formdata(self, valuelist):
        # valuelist will be [b''] if no files uploaded, so set data to None
        if valuelist == [b'']:
            self.data = None
        elif valuelist == []:
            raise ValueError(self.gettext('Only accept file(s).'))
        else:
            self.data = []
            for i in valuelist:
                if isinstance(i, _FieldStorage):
                    self.data.append(i)
                elif isinstance(i, _CGIFieldStorage):
                    self.data.append(_FieldStorage(i))
                else:
                    raise ValueError(self.gettext('Only accept file(s).'))

class MultipleCheckboxField(SelectMultipleField):
    """Handle multiple checkbox list"""

    widget = _ListWidget(prefix_label=False)
    option_widget = _CheckboxInput()
