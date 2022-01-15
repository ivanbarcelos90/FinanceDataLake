import app


def test_app_passed():
    assert app.power(2, 2) == 4
    assert app.power(-2, 2) == 4


def test_app_failure():
    assert app.power(3, 3) == 9
