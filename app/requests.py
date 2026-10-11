from app.fields import FieldValidationError


class MethodRequest:
    def __init__(self, data: dict):
        if data is None:
            data = {}
        self._raw = data

        if type(self) is MethodRequest:
            self._validate_required()


    def _validate_required(self):
        if not self._raw.get("method"):
            raise FieldValidationError("method is required")
        if not self._raw.get("token"):
            raise FieldValidationError("token is required")
        if not self._raw.get("login"):
            raise FieldValidationError("login is required")


    @property
    def method(self) -> str | None:
        return self._raw.get("method")


    @property
    def token(self) -> str | None:
        return self._raw.get("token")


    @property
    def login(self) -> str | None:
        return self._raw.get("login")


    @property
    def account(self):
        val = self._raw.get("account")
        if val is None:
            return None
        if not isinstance(val, str):
            raise FieldValidationError("account must be a string or null")
        s = val.strip()
        return s if s else None


class ClientsInterestsRequest(MethodRequest):
    def __init__(self, data: dict):
        super().__init__(data)
        _ = self.client_ids
        _ = self.date


    @property
    def client_ids(self):
        raw = self._raw.get("client_ids")
        if raw is None:
            raise FieldValidationError("client_ids is required")
        if not isinstance(raw, list):
            raise FieldValidationError("client_ids must be a list")
        for i, cid in enumerate(raw):
            if not isinstance(cid, int):
                raise FieldValidationError(f"client_ids[{i}] must be an integer")
        return raw


    @property
    def date(self):
        return self._raw.get("date")


class OnlineScoreRequest(MethodRequest):
    def __init__(self, data: dict):
        if data is None:
            data = {}

        raw_gender = data.get("gender")
        if raw_gender is not None and isinstance(raw_gender, int):
            data["gender"] = str(raw_gender)

        super().__init__(data)

        _ = self.phone
        _ = self.email
        _ = self.first_name
        _ = self.last_name
        _ = self.gender
        _ = self.birthday

        has_phone_email = bool(self.phone and self.email)
        has_first_last = bool(self.first_name and self.last_name)
        has_gender_birthday = bool(self.gender is not None and self.birthday)

        any_data = (
            self.phone is not None or
            self.email is not None or
            self.first_name is not None or
            self.last_name is not None or
            self.gender is not None or
            self.birthday is not None
        )

        if any_data and not (has_phone_email or has_first_last or has_gender_birthday):
            raise FieldValidationError(
                "At least one valid pair must be provided: "
                "(phone & email) OR (first_name & last_name) OR (gender & birthday)"
            )


    @property
    def phone(self):
        return self._raw.get("phone")


    @property
    def email(self):
        return self._raw.get("email")


    @property
    def first_name(self):
        return self._raw.get("first_name")


    @property
    def last_name(self):
        return self._raw.get("last_name")


    @property
    def gender(self):
        return self._raw.get("gender")


    @property
    def birthday(self):
        return self._raw.get("birthday")
