from builtins import range
import pytest
from sqlalchemy import select
from app.dependencies import get_settings
from app.models.user_model import User
from app.services.user_service import UserService
from unittest.mock import patch
from fastapi import HTTPException

pytestmark = pytest.mark.asyncio

# Test creating a user with valid data
async def test_create_user_with_valid_data(db_session, email_service):
    user_data = {
        "email": "valid_user@example.com",
        "password": "ValidPassword123!",
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is not None
    assert user.email == user_data["email"]

# Test creating a user with invalid data
async def test_create_user_with_invalid_data(db_session, email_service):
    user_data = {
        "nickname": "",  # Invalid nickname
        "email": "invalidemail",  # Invalid email
        "password": "short",  # Invalid password
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is None

# Test fetching a user by ID when the user exists
async def test_get_by_id_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_id(db_session, user.id)
    assert retrieved_user.id == user.id

# Test fetching a user by ID when the user does not exist
async def test_get_by_id_user_does_not_exist(db_session):
    non_existent_user_id = "non-existent-id"
    retrieved_user = await UserService.get_by_id(db_session, non_existent_user_id)
    assert retrieved_user is None

# Test fetching a user by nickname when the user exists
async def test_get_by_nickname_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_nickname(db_session, user.nickname)
    assert retrieved_user.nickname == user.nickname

# Test fetching a user by nickname when the user does not exist
async def test_get_by_nickname_user_does_not_exist(db_session):
    retrieved_user = await UserService.get_by_nickname(db_session, "non_existent_nickname")
    assert retrieved_user is None

# Test fetching a user by email when the user exists
async def test_get_by_email_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_email(db_session, user.email)
    assert retrieved_user.email == user.email

# Test fetching a user by email when the user does not exist
async def test_get_by_email_user_does_not_exist(db_session):
    retrieved_user = await UserService.get_by_email(db_session, "non_existent_email@example.com")
    assert retrieved_user is None

# Test updating a user with valid data
async def test_update_user_valid_data(db_session, user):
    new_email = "updated_email@example.com"
    updated_user = await UserService.update(db_session, user.id, {"email": new_email})
    assert updated_user is not None
    assert updated_user.email == new_email

# Test updating a user with invalid data
async def test_update_user_invalid_data(db_session, user):
    updated_user = await UserService.update(db_session, user.id, {"email": "invalidemail"})
    assert updated_user is None

# Test deleting a user who exists
async def test_delete_user_exists(db_session, user):
    deletion_success = await UserService.delete(db_session, user.id)
    assert deletion_success is True

# Test attempting to delete a user who does not exist
async def test_delete_user_does_not_exist(db_session):
    non_existent_user_id = "non-existent-id"
    deletion_success = await UserService.delete(db_session, non_existent_user_id)
    assert deletion_success is False

# Test listing users with pagination
async def test_list_users_with_pagination(db_session, users_with_same_role_50_users):
    users_page_1 = await UserService.list_users(db_session, skip=0, limit=10)
    users_page_2 = await UserService.list_users(db_session, skip=10, limit=10)
    assert len(users_page_1) == 10
    assert len(users_page_2) == 10
    assert users_page_1[0].id != users_page_2[0].id

# Test registering a user with valid data
async def test_register_user_with_valid_data(db_session, email_service):
    user_data = {
        "email": "register_valid_user@example.com",
        "password": "RegisterValid123!",
    }
    user = await UserService.register_user(db_session, user_data, email_service)
    assert user is not None
    assert user.email == user_data["email"]

# Test attempting to register a user with invalid data
async def test_register_user_with_invalid_data(db_session, email_service):
    user_data = {
        "email": "registerinvalidemail",  # Invalid email
        "password": "short",  # Invalid password
    }
    user = await UserService.register_user(db_session, user_data, email_service)
    assert user is None

# Test successful user login
async def test_login_user_successful(db_session, verified_user):
    user_data = {
        "email": verified_user.email,
        "password": "MySuperPassword$1234",
    }
    logged_in_user = await UserService.login_user(db_session, user_data["email"], user_data["password"])
    assert logged_in_user is not None

# Test user login with incorrect email
async def test_login_user_incorrect_email(db_session):
    user = await UserService.login_user(db_session, "nonexistentuser@noway.com", "Password123!")
    assert user is None

# Test user login with incorrect password
async def test_login_user_incorrect_password(db_session, user):
    user = await UserService.login_user(db_session, user.email, "IncorrectPassword!")
    assert user is None

# Test account lock after maximum failed login attempts
async def test_account_lock_after_failed_logins(db_session, verified_user):
    max_login_attempts = get_settings().max_login_attempts
    for _ in range(max_login_attempts):
        await UserService.login_user(db_session, verified_user.email, "wrongpassword")
    
    is_locked = await UserService.is_account_locked(db_session, verified_user.email)
    assert is_locked, "The account should be locked after the maximum number of failed login attempts."

# Test resetting a user's password
async def test_reset_password(db_session, user):
    new_password = "NewPassword123!"
    reset_success = await UserService.reset_password(db_session, user.id, new_password)
    assert reset_success is True

# Test verifying a user's email
async def test_verify_email_with_token(db_session, user):
    token = "valid_token_example"  # This should be set in your user setup if it depends on a real token
    user.verification_token = token  # Simulating setting the token in the database
    await db_session.commit()
    result = await UserService.verify_email_with_token(db_session, user.id, token)
    assert result is True

# Test unlocking a user's account
async def test_unlock_user_account(db_session, locked_user):
    unlocked = await UserService.unlock_user_account(db_session, locked_user.id)
    assert unlocked, "The account should be unlocked"
    refreshed_user = await UserService.get_by_id(db_session, locked_user.id)
    assert not refreshed_user.is_locked, "The user should no longer be locked"

base_user_data = {
    "email": "base_user@example.com",
    "password": "ValidPassword123!",
    "nickname": "base_nickname",
}

# Helper function for user registration tests
async def register_user_helper(db_session, email_service, user_data):
    return await UserService.register_user(db_session, user_data, email_service)

# Test registering a user with a provided nickname
async def test_register_with_valid_nickname(db_session, email_service):
    user_data = base_user_data.copy()
    user_data.update({
        "nickname": "unique_nickname_123",
    })
    user = await register_user_helper(db_session, email_service, user_data)
    assert user is not None
    assert user.email == user_data["email"]
    assert user.nickname == user_data["nickname"]

# Test registering a user without a nickname
@patch('app.services.user_service.logger')
async def test_register_without_nickname(mock_logger, db_session, email_service):
    user_data = base_user_data.copy()
    user_data.pop("nickname")
    with pytest.raises(HTTPException) as exc_info:
        await register_user_helper(db_session, email_service, user_data)
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "No nickname provided"
    mock_logger.error.assert_called_with("No nickname provided.")

# Test registering a user with an invalid nickname (empty string)
@patch('app.services.user_service.logger')
async def test_register_invalid_nickname(mock_logger, db_session, email_service):
    user_data = base_user_data.copy()
    user_data.update({
        "nickname": ""
    })
    with pytest.raises(HTTPException) as exc_info:
        await register_user_helper(db_session, email_service, user_data)
    assert exc_info.value.status_code == 422
    mock_logger.error.assert_called()

# Test registering a user with an already taken nickname
@patch('app.services.user_service.logger')
async def test_register_taken_nickname(mock_logger, db_session, email_service):
    # Create the first user with a unique nickname
    user_data_1 = base_user_data.copy()
    user_data_1.update({
        "nickname": "unique_nickname_123",
    })
    first_user = await register_user_helper(db_session, email_service, user_data_1)
    assert first_user is not None
    assert first_user.email == user_data_1["email"]
    assert first_user.nickname == user_data_1["nickname"]

    # Attempt to create a second user with the same nickname
    user_data_2 = base_user_data.copy()
    user_data_2.update({
        "nickname": "unique_nickname_123",  # Same nickname as the first user
        "email": "different_email@example.com"  # Different email to test nickname uniqueness
    })
    with pytest.raises(HTTPException) as exc_info:
        await register_user_helper(db_session, email_service, user_data_2)
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Nickname already exists"
    mock_logger.error.assert_called_with("User with given nickname already exists.")

# Test registering a user with a nickname that exceeds 30 characters
@patch('app.services.user_service.logger')
async def test_register_user_long_nickname(mock_logger, db_session, email_service):
    user_data = base_user_data.copy()
    user_data.update({
        "nickname": "this_nickname_is_way_too_long_and_exceeds_30_characters",
    })
    with pytest.raises(HTTPException) as exc_info:
        await register_user_helper(db_session, email_service, user_data)
    assert exc_info.value.status_code == 422
    mock_logger.error.assert_called()

# Test registering a user with a nickname containing disallowed special characters
@patch('app.services.user_service.logger')
async def test_register_disallowed_characters_nickname(mock_logger, db_session, email_service):
    user_data = base_user_data.copy()
    user_data.update({
        "nickname": "invalid_nickname$%",
    })
    with pytest.raises(HTTPException) as exc_info:
        await register_user_helper(db_session, email_service, user_data)
    assert exc_info.value.status_code == 422
    mock_logger.error.assert_called()