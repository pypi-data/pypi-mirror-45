__all__ = ['WebPageSchema']

from quaerere_base_common.schema import BaseSchema
from ..models import WebPageBase


class WebPageSchema(WebPageBase, BaseSchema):
    pass
