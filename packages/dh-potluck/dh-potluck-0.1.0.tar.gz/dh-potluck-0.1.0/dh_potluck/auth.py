import re
from http import HTTPStatus

from flask import g, jsonify, request

token_missing = {
    'description': 'Authentication token missing or incorrectly formatted.',
    'status': HTTPStatus.UNAUTHORIZED,
}
token_invalid = {
    'description': 'Authentication token invalid or expired.',
    'status': HTTPStatus.UNAUTHORIZED,
}
auth_error = {
    'description': 'An error occurred trying to authenticate.',
    'status': HTTPStatus.INTERNAL_SERVER_ERROR,
}


def error_response(error):
    return jsonify({'description': error['description']}), error['status']


class UnauthenticatedUser:
    pass


class ApplicationUser:
    pass


def get_user(app_token, token_model):
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        g.user = UnauthenticatedUser()
        return

    match = re.match('^(Application|Bearer) ([a-z0-9]+)$', auth_header)
    if not match:
        return error_response(token_missing)

    # Application token
    if match.group(1) == 'Application':
        if match.group(2) == app_token:
            g.user = ApplicationUser()
        else:
            return error_response(token_invalid)

    # Bearer token
    elif match.group(1) == 'Bearer':
        token = token_model.query.filter_by(token=match.group(2)).first()
        if not token or (token and token.is_expired):
            return error_response(token_invalid)

        g.user = token.user
