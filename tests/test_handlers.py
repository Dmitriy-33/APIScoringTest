import datetime
from unittest.mock import Mock
from app.handlers import handle_online_score, handle_clients_interests


class TestClientsInterestsHandler:
    def test_empty_client_ids_fails_validation(self):
        data = {
            "method": "clients_interests",
            "token": "valid_token",
            "login": "admin",
            "client_ids": [],
        }
        resp, status = handle_clients_interests(data, {}, Mock())
        assert status == 400


    def test_non_int_client_id_fails_validation(self):
        data = {
            "method": "clients_interests",
            "token": "valid_token",
            "login": "admin",
            "client_ids": ["1", 2, 3],
        }
        resp, status = handle_clients_interests(data, {}, Mock())
        assert status == 400


    def test_store_get_interests_called_once_per_id(self):
        client_ids = [1, 2, 3]
        data = {
            "method": "clients_interests",
            "token": "valid_token",
            "login": "admin",
            "client_ids": client_ids,
        }
        store_mock = Mock()
        store_mock.get_interests.side_effect = lambda cid: [f"interest_{cid}"]

        resp, status = handle_clients_interests(data, {}, store_mock)
        assert status == 200
        assert "interests" in resp
        assert store_mock.get_interests.call_count == len(client_ids)


    def test_valid_client_ids_returns_interests(self):
        data = {
            "method": "clients_interests",
            "token": "valid_token",
            "login": "admin",
            "client_ids": [10, 20],
        }
        store_mock = Mock()
        store_mock.get_interests.side_effect = lambda cid: ["sport", "tech"]

        resp, status = handle_clients_interests(data, {}, store_mock)
        assert status == 200
        assert "interests" in resp
        assert isinstance(resp["interests"], dict)


class TestOnlineScoreHandler:
    def test_invalid_phone_format_returns_400(self):
        data = {
            "method": "online_score",
            "token": "valid_token",
            "login": "admin",
            "phone": "123",  # неверный формат
            "email": "test@example.com",
        }
        resp, status = handle_online_score(data, {}, Mock())
        assert status == 400


    def test_no_valid_pair_returns_400(self):
        data = {
            "method": "online_score",
            "token": "valid_token",
            "login": "admin",
            "phone": "+79990000000",
            # email отсутствует — нет валидной пары
        }
        resp, status = handle_online_score(data, {}, Mock())
        assert status == 400


    def test_score_depends_on_current_hour(self):
        hour = datetime.datetime.now().hour
        data = {
            "method": "online_score",
            "token": "valid_token",
            "login": "admin",
            "phone": "+79990000000",
            "email": "test@example.com",
        }
        resp, status = handle_online_score(data, {}, Mock())
        assert status == 200
        expected_base = 10 + 5  # phone & email
        expected = expected_base + (hour % 10)
        assert resp["score"] == expected


    def test_valid_first_last_name_pair(self):
        data = {
            "method": "online_score",
            "token": "valid_token",
            "login": "admin",
            "first_name": "Ivan",
            "last_name": "Petrov",
        }
        resp, status = handle_online_score(data, {}, Mock())
        assert status == 200
        assert resp["score"] >= 14


    def test_valid_gender_birthday_pair(self):
        data = {
            "method": "online_score",
            "token": "valid_token",
            "login": "admin",
            "gender": "m",
            "birthday": "1990-01-01",
        }
        resp, status = handle_online_score(data, {}, Mock())
        assert status == 200
        assert resp["score"] >= 13


    def test_valid_phone_email_pair(self):
        data = {
            "method": "online_score",
            "token": "valid_token",
            "login": "admin",
            "phone": "+79991112233",
            "email": "user@example.com",
        }
        resp, status = handle_online_score(data, {}, Mock())
        assert status == 200
        assert resp["score"] >= 15
