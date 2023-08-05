import importlib

from .auth import get_user


class DHPotluck:
    def __init__(self, app=None, **kwargs):
        """Initialize dh-potluck."""
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        app_token = app.config['DH_POTLUCK_APP_TOKEN']
        module_name, class_name = app.config['DH_POTLUCK_TOKEN_MODEL'].rsplit('.', 1)
        token_model = getattr(importlib.import_module(module_name), class_name)

        @app.before_request
        def before_request():
            return get_user(app_token, token_model)
