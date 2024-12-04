import pytest
from app.utils.validation import validate_nickname

@pytest.mark.parametrize("nickname,expected_valid", [
    ("john123", True),
    ("john-doe", True),
    ("john_doe", True),
    ("a" * 30, True),
    ("123user", True),
    ("user123", True),
    # Invalid cases
    ("jo", False),  # Too short
    ("a" * 31, False),  # Too long
    ("admin", False),  # Reserved word
    ("user--name", False),  # Consecutive special chars
    ("-username", False),  # Starts with special char
    ("username-", False),  # Ends with special char
    ("user@name", False),  # Invalid character
    ("user name", False),  # Space not allowed
    ("user__name", False),  # Consecutive special chars
])
def test_nickname_validation(nickname, expected_valid):
    is_valid, error_message = validate_nickname(nickname)
    assert is_valid == expected_valid, f"Failed for nickname: {nickname}, error: {error_message}" 