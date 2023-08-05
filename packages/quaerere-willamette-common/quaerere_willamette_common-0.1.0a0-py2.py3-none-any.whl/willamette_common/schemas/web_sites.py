__all__ = ['WebSiteSchema']

from quaerere_base_common.schema import BaseSchema
from ..models import WebSiteBase


class WebSiteSchema(WebSiteBase, BaseSchema):
    pass
