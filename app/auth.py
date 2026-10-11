from __future__ import annotations

import datetime
import hashlib

from app.requests import MethodRequest

SALT = "Otus"
ADMIN_SALT = "42"
ADMIN_LOGIN = "admin"


def _make_digest(message: str) -> str:
    return hashlib.sha512(message.encode("utf-8")).hexdigest()


def check_auth(request: MethodRequest) -> bool:
    if request.is_admin:
        hour_str = datetime.datetime.now().strftime("%Y%m%d%H")
        message = f"{hour_str}{ADMIN_SALT}"
    else:
        account = request.account or ""
        login = request.login or ""
        message = f"{account}{login}{SALT}"

    return _make_digest(message) == request.token
