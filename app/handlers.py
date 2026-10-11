import datetime
from app.requests import OnlineScoreRequest, ClientsInterestsRequest
from app.fields import FieldValidationError


def _validate_basic_auth(data: dict) -> None:
    if not data.get("method"):
        raise FieldValidationError("method is required")
    if not data.get("token"):
        raise FieldValidationError("token is required")
    if not data.get("login"):
        raise FieldValidationError("login is required")


def handle_online_score(arguments: dict, ctx: dict, store) -> tuple[dict, int]:
    try:
        _validate_basic_auth(arguments)
        req = OnlineScoreRequest(arguments)
    except FieldValidationError as e:
        return {"error": str(e)}, 400

    current_hour = datetime.datetime.now().hour

    score = 10
    if req.phone and req.email:
        score += 5
    elif req.first_name and req.last_name:
        score += 4
    elif req.gender is not None and req.birthday:
        score += 3

    score += current_hour % 10

    return {"score": score}, 200


def handle_clients_interests(arguments: dict, ctx: dict, store) -> tuple[dict, int]:
    try:
        _validate_basic_auth(arguments)
        req = ClientsInterestsRequest(arguments)
    except FieldValidationError as e:
        return {"error": str(e)}, 400

    client_ids = req.client_ids
    if not client_ids:
        return {"error": "client_ids cannot be empty"}, 400

    interests = {}
    for cid in client_ids:
        interests[str(cid)] = store.get_interests(cid)

    return {"interests": interests}, 200
