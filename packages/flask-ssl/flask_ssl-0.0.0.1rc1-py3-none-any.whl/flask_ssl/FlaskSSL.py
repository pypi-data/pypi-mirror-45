from functools import wraps
from flask import request, redirect


def is_secure():
    return (request.is_secure or
            request.headers.get('X-Forwarded-Proto') == 'https' or
            request.headers.get('HTTPS') == 'on')


def _ssl_req(fn, action=None):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if is_secure():
            return fn(*args, **kwargs)
        else:
            return action()

    return decorated_view


def ssl_require(fn):
    """
    SSL Required annotation
    """
    def require():
        return "SSL Required", 426

    return _ssl_req(fn, action=require)


def ssl_redirect(fn):
    """
    SSL Redirect annotation
    """
    def upgrade():
        return redirect(request.url.replace("http://", "https://"))

    return _ssl_req(fn, action=upgrade)


__all__ = ["ssl_require", "ssl_redirect", ]
