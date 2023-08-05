import importlib

from flask import g

from .auth import role_required, get_user


class DHPotluck:
    def __init__(self, app=None, **kwargs):
        """Initialize dh-potluck."""
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        app_token = app.config['DH_POTLUCK_APP_TOKEN']
        module_name, class_name = app.config['DH_POTLUCK_VALIDATE_TOKEN_FUNC'].rsplit('.', 1)
        validate_token_func = getattr(importlib.import_module(module_name), class_name)

        @app.before_request
        def before_request():
            return get_user(app_token, validate_token_func)

    @staticmethod
    def role_required(*args, **kwargs):
        return role_required(*args, **kwargs)

    @property
    def current_user(self):
        return g.user
