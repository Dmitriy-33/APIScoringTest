import unittest
from datetime import datetime, timedelta

from app.fields import (
    CharField,
    EmailField,
    PhoneField,
    DateField,
    BirthDayField,
    GenderField,
    ClientIDsField,
    FieldValidationError,
)


class TestCharField(unittest.TestCase):
    def test_valid_string(self):
        class Container:
            name = CharField(required=True)

        c = Container()
        c.name = "Ivan"
        self.assertEqual(c.name, "Ivan")


    def test_non_string_raises(self):
        class Container:
            name = CharField(required=True)

        c = Container()
        with self.assertRaises(FieldValidationError):
            c.name = 123


    def test_nullable_none(self):
        class Container:
            name = CharField(required=False, nullable=True)

        c = Container()
        c.name = None
        self.assertIsNone(c.name)


    def test_required_empty_string_fails(self):
        class Container:
            name = CharField(required=True, nullable=False)

        c = Container()
        with self.assertRaises(FieldValidationError):
            c.name = ""


class TestEmailField(unittest.TestCase):
    def test_valid_email(self):
        class Container:
            email = EmailField(required=True)

        c = Container()
        c.email = "ivan@example.com"
        self.assertEqual(c.email, "ivan@example.com")


    def test_missing_at_fails(self):
        class Container:
            email = EmailField(required=True)

        c = Container()
        with self.assertRaises(FieldValidationError):
            c.email = "ivanexample.com"


    def test_none_with_nullable_ok(self):
        class Container:
            email = EmailField(required=False, nullable=True)

        c = Container()
        c.email = None
        self.assertIsNone(c.email)


class TestPhoneField(unittest.TestCase):
    def test_valid_phone(self):
        class Container:
            phone = PhoneField(required=True)

        c = Container()
        c.phone = "79991234567"
        self.assertEqual(c.phone, "79991234567")


    def test_int_phone_ok(self):
        class Container:
            phone = PhoneField(required=True)

        c = Container()
        c.phone = 79991234567
        self.assertEqual(c.phone, 79991234567)


    def test_wrong_length_fails(self):
        class Container:
            phone = PhoneField(required=True)

        c = Container()
        with self.assertRaises(FieldValidationError):
            c.phone = "7123456789"  # 10 digits


    def test_not_starting_with_7_fails(self):
        class Container:
            phone = PhoneField(required=True)

        c = Container()
        with self.assertRaises(FieldValidationError):
            c.phone = "89991234567"


    def test_letters_in_phone_fails(self):
        class Container:
            phone = PhoneField(required=True)

        c = Container()
        with self.assertRaises(FieldValidationError):
            c.phone = "7abcdefghij"


class TestDateField(unittest.TestCase):
    DATE_FORMAT = "%d.%m.%Y"


    def test_valid_date(self):
        class Container:
            date = DateField(required=True)

        c = Container()
        c.date = "01.01.2020"
        self.assertEqual(c.date, "01.01.2020")


    def test_invalid_format_fails(self):
        class Container:
            date = DateField(required=True)

        c = Container()
        with self.assertRaises(FieldValidationError):
            c.date = "2020-01-01"


    def test_future_date_fails(self):
        class Container:
            date = DateField(required=True)

        c = Container()
        tomorrow = (datetime.now() + timedelta(days=1)).strftime(self.DATE_FORMAT)
        with self.assertRaises(FieldValidationError):
            c.date = tomorrow


class TestBirthDayField(unittest.TestCase):
    DATE_FORMAT = "%d.%m.%Y"


    def test_valid_birthday(self):
        class Container:
            birthday = BirthDayField(required=True)

        c = Container()
        c.birthday = "01.01.1990"
        self.assertEqual(c.birthday, "01.01.1990")


    def test_too_old_fails(self):
        class Container:
            birthday = BirthDayField(required=True)

        c = Container()
        old_date = (datetime.now() - timedelta(days=71 * 365)).strftime(self.DATE_FORMAT)
        with self.assertRaises(FieldValidationError):
            c.birthday = old_date


class TestGenderField(unittest.TestCase):
    def test_allowed_values(self):
        class Container:
            gender = GenderField(required=True)

        c = Container()
        for v in [0, 1, 2]:
            c.gender = v
            self.assertEqual(c.gender, v)


    def test_disallowed_value_fails(self):
        class Container:
            gender = GenderField(required=True)

        c = Container()
        with self.assertRaises(FieldValidationError):
            c.gender = 3


    def test_bool_rejected(self):
        class Container:
            gender = GenderField(required=True)

        c = Container()
        with self.assertRaises(FieldValidationError):
            c.gender = True


class TestClientIDsField(unittest.TestCase):
    def test_valid_list(self):
        class Container:
            client_ids = ClientIDsField(required=True)

        c = Container()
        c.client_ids = [101, 102]
        self.assertEqual(c.client_ids, [101, 102])


    def test_empty_list_fails(self):
        class Container:
            client_ids = ClientIDsField(required=True)

        c = Container()
        with self.assertRaises(FieldValidationError):
            c.client_ids = []


    def test_non_int_item_fails(self):
        class Container:
            client_ids = ClientIDsField(required=True)

        c = Container()
        with self.assertRaises(FieldValidationError):
            c.client_ids = [101, "abc"]


if __name__ == "__main__":
    unittest.main()
