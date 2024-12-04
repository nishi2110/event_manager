import pytest
from app.utils.validation import validate_nickname, validate_password

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

@pytest.mark.parametrize("password,expected_valid", [
    ("SecurePass123!", True),  # Valid password
    ("Ab1!defgh", True),       # Minimum length with all requirements
    ("Ab1!" + "a"*124, True),  # Maximum length
    # Invalid cases
    ("", False),               # Empty password
    ("short", False),          # Too short
    ("lowercase123!", False),  # No uppercase
    ("UPPERCASE123!", False),  # No lowercase
    ("Abcdefghi!", False),    # No numbers
    ("Abcdefgh123", False),   # No special characters
    ("a"*129, False),         # Too long
    (" ", False),             # Just whitespace
    ("Pass word1!", False),   # Contains space
])
def test_password_validation(password, expected_valid):
    """Test password validation with various cases"""
    is_valid, error_message = validate_password(password)
    assert is_valid == expected_valid, f"Failed for password: {password}, error: {error_message}" 