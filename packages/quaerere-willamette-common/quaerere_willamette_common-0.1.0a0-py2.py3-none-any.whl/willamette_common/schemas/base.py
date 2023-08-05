__all__ = 'BaseSchema'

from marshmallow import Schema, post_load


class BaseSchema(Schema):

    def __init__(self, model_class, *args, **kwargs):
        self.model_class = model_class
        super().__init__(*args, **kwargs)

    @post_load
    def make_web_site(self, data):
        return self.model_class(**data)
