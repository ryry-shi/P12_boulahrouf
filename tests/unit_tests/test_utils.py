import datetime
import utils
from utils import (
    email_validator,
    future_date_validator,
    int_validator,
    past_date_validator,
    str_validator,
    phone_validator,
    password_validator,
    positive_int_validator,
    two_date_validator,
    user_input,
    submit_form,
    ask_user_choice
)
import pytest
import mock
import builtins


def test_str_validator():
    assert str_validator("ploupisme") == "ploupisme"
    assert str_validator("") == None
    with pytest.raises(ValueError): 
        str_validator("test")
    assert type(str_validator("ploupisme")) == str


def test_phone_validator():
    assert phone_validator("0102030405") == "0102030405" 
    assert phone_validator("") == None
    with pytest.raises(ValueError):
        phone_validator("12345")
        phone_validator("123459875444456")
        phone_validator("saas!axaxaxa")
        

def test_password_validator():
    assert password_validator("12345678") == "12345678"
    assert password_validator("") == None
    with pytest.raises(ValueError):
        password_validator("1234567")


def test_int_validator():
    assert int_validator("1") == 1
    assert int_validator("") == None
    with pytest.raises(ValueError):
        int_validator("a")


def test_email_validator():
    assert email_validator("ryry@email.fr") == "ryry@email.fr"
    assert email_validator("") == None
    with pytest.raises(ValueError):
        email_validator("ryry")
        email_validator("ryry@")
        email_validator("ryry@hotmail")
        email_validator("ryry@hotmail.")
        email_validator("ryry@hotmail.fr")
        email_validator("@hotmail.fr")
        email_validator("ryry@hot mail.fr")


def test_date_validator():
    assert past_date_validator("2000-10-10") == datetime.datetime.fromisoformat("2000-10-10")
    assert past_date_validator("") == None
    with pytest.raises(ValueError):
        past_date_validator("2000.10.40")
        past_date_validator("2000/13/10")
        past_date_validator("2000-02-30")
        past_date_validator("12-2020-01")


def test_future_date_validator():
    assert future_date_validator("9999-11-11") == datetime.datetime.fromisoformat("9999-11-11")
    assert future_date_validator("") == None
    with pytest.raises(ValueError):
        future_date_validator("2000-10-10")
        future_date_validator("9999/11/11")
        future_date_validator("9999-11-11")
        future_date_validator("11-9999-11")

def test_past_date_validator():
    assert past_date_validator("2000-11-11") == datetime.datetime.fromisoformat("2000-11-11")
    assert past_date_validator("") == None
    with pytest.raises(ValueError):
        past_date_validator("2000.10.40")
        past_date_validator("2000/13/10")
        past_date_validator("9999-10-10")
        past_date_validator("12-2020-01")
        
        
def test_two_date_validator():
    assert two_date_validator("2022-01-01", "2023-01-01") != None
    with pytest.raises(ValueError):
        two_date_validator("2023-01-01", "2022-01-01")

def test_positive_int_validator():
    with mock.patch.object(utils, 'positive_int_validator', lambda x: int(x)):
        assert positive_int_validator("1") == 1
        assert positive_int_validator("") == None
        with pytest.raises(ValueError):
            positive_int_validator("-1")


def test_user_input():
    with mock.patch.object(builtins, 'input', lambda _: 'tadatatatata'): 
        assert user_input("test", str_validator) == 'tadatatatata'
    with mock.patch.object(builtins, 'input', lambda _: "42"): 
        assert user_input("test", int_validator) == 42
    


def test_submit_form():
    def mocked_user_input(message, validator):
        match validator.__name__:
            case "int_validator":
                return 42
            case "str_validator":
                return "ryad"
            case "email_validator":
                return "ryad@boulahrouf.fr"
    with mock.patch.object(utils, 'user_input', mocked_user_input):
        assert submit_form("test", [
            {"name": "id", "description": "ID", "validator": int_validator},
            {"name": "name", "description": "Nom", "validator": str_validator},
            {"name": "email", "description": "Email", "validator": email_validator},
        ]) == {
            "id": 42, "name": "ryad", "email": "ryad@boulahrouf.fr"
        }


def test_ask_user_choice():
    with mock.patch.object(builtins, 'input', lambda _: "2"): 
        assert ask_user_choice(3) == 1
