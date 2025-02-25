from wtforms.widgets import html_params
from markupsafe import Markup

class LinkWidget(object):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('href', field.data or '')
        kwargs.setdefault('target', '_blank')
        return Markup('<a {}>{}</a>'.format(html_params(**kwargs), field.data))
