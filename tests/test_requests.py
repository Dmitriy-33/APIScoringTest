import unittest
from app.requests import MethodRequest, ClientsInterestsRequest, OnlineScoreRequest
from app.fields import FieldValidationError


class TestMethodRequest(unittest.TestCase):
    def test_required_fields_present(self):
        data = {
            "method": "online_score",
            "token": "secret_token",
            "login": "admin",
            "account": "my_account"
        }
        req = MethodRequest(data)
        self.assertEqual(req.method, "online_score")
        self.assertEqual(req.token, "secret_token")
        self.assertEqual(req.login, "admin")
        self.assertEqual(req.account, "my_account")


    def test_missing_method_fails(self):
        data = {"token": "secret", "login": "user"}
        with self.assertRaises(FieldValidationError):
            MethodRequest(data)


    def test_missing_token_fails(self):
        data = {"method": "test", "login": "user"}
        with self.assertRaises(FieldValidationError):
            MethodRequest(data)


    def test_missing_login_fails(self):
        data = {"method": "test", "token": "secret"}
        with self.assertRaises(FieldValidationError):
            MethodRequest(data)


    def test_account_optional(self):
        data = {"method": "test", "token": "secret", "login": "user"}
        req = MethodRequest(data)
        self.assertIsNone(req.account)


    def test_missing_arguments_fails(self):
        data = {}
        with self.assertRaises(FieldValidationError):
            MethodRequest(data)


class TestClientsInterestsRequest(unittest.TestCase):
    def test_client_ids_required(self):
        data = {"client_ids": [101, 102], "date": "01.01.2020"}
        req = ClientsInterestsRequest(data)
        self.assertEqual(req.client_ids, [101, 102])
        self.assertEqual(req.date, "01.01.2020")


    def test_date_optional(self):
        data = {"client_ids": [101]}
        req = ClientsInterestsRequest(data)
        self.assertEqual(req.client_ids, [101])
        self.assertIsNone(req.date)


    def test_missing_client_ids_fails(self):
        data = {"date": "01.01.2020"}
        with self.assertRaises(FieldValidationError):
            ClientsInterestsRequest(data)


class TestOnlineScoreRequest(unittest.TestCase):
    def test_valid_phone_email_pair(self):
        data = {"phone": "79991234567", "email": "ivan@example.com"}
        req = OnlineScoreRequest(data)
        self.assertEqual(req.phone, "79991234567")
        self.assertEqual(req.email, "ivan@example.com")


    def test_valid_first_last_name_pair(self):
        data = {"first_name": "Ivan", "last_name": "Petrov"}
        req = OnlineScoreRequest(data)
        self.assertEqual(req.first_name, "Ivan")
        self.assertEqual(req.last_name, "Petrov")


    def test_valid_gender_birthday_pair(self):
        data = {"gender": 1, "birthday": "1990-05-10"}
        req = OnlineScoreRequest(data)
        self.assertEqual(req.gender, "1")
        self.assertEqual(req.birthday, "1990-05-10")


    def test_no_valid_pair_fails(self):
        data = {
            "method": "online_score",
            "token": "valid_token",
            "login": "admin",
            "phone": "+79991234567",
        }
        with self.assertRaises(FieldValidationError):
            OnlineScoreRequest(data)

