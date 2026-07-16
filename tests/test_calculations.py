import pytest
from app.calculations import add

@pytest.mark.parametrize("a, b, result",[
    (1, 2, 3),
    (2, 9, 11),
    (10, 10, 20)
])

# Fixture syntex:
# @pytest.fixture
# def zero_bank_account():
#     return bank_account(0)

def test_add(a, b, result):
    print("Testing...")
    assert add(a, b) == result