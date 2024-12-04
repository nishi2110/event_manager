from builtins import str
import pytest
from httpx import AsyncClient
from app.main import app
from app.models.user_model import User
from app.utils.nickname_gen import generate_nickname
from app.utils.security import hash_password
from app.services.jwt_service import decode_token  # Import your FastAPI app
from urllib.parse import urlencode
from uuid import uuid4

# Example of a test function using the async_client fixture
@pytest.mark.asyncio
async def test_create_user_access_denied(async_client, user_token, email_service):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Define user data for the test
    user_data = {
        "nickname": generate_nickname(),
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
    }
    # Send a POST request to create a user
    response = await async_client.post("/users/", json=user_data, headers=headers)
    # Asserts
    assert response.status_code == 403

# You can similarly refactor other test functions to use the async_client fixture
@pytest.mark.asyncio
async def test_retrieve_user_access_denied(async_client, verified_user, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.get(f"/users/{verified_user.id}", headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_retrieve_user_access_allowed(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == str(admin_user.id)

@pytest.mark.asyncio
async def test_update_user_email_access_denied(async_client, verified_user, user_token):
    updated_data = {"email": f"updated_{verified_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(f"/users/{verified_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_user_email_access_allowed(async_client, admin_user, admin_token):
    updated_data = {"email": f"updated_{admin_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == updated_data["email"]


@pytest.mark.asyncio
async def test_delete_user(async_client, admin_token_headers, test_user):
    response = await async_client.delete(
        f"/users/{test_user.id}",
        headers=admin_token_headers
    )
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_create_user_duplicate_email(async_client, test_user):
    response = await async_client.post(
        "/register/",  # Changed from "/users/" to "/register/"
        json={
            "email": test_user.email,
            "password": "testpassword123"
            # Removed nickname as it's not in the working example
        }
    )
    assert response.status_code == 500
    assert "Email already exists" in response.json().get("detail", "")  # Added error message check

@pytest.mark.asyncio
async def test_create_user_invalid_email(async_client):
    user_data = {
        "email": "notanemail",
        "password": "ValidPassword123!",
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_login_success(async_client, verified_user):
    # Attempt to login with the test user
    form_data = {
        "username": verified_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    # Check for successful login response
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Use the decode_token method from jwt_service to decode the JWT
    decoded_token = decode_token(data["access_token"])
    assert decoded_token is not None, "Failed to decode token"
    assert decoded_token["role"] == "AUTHENTICATED", "The user role should be AUTHENTICATED"

@pytest.mark.asyncio
async def test_login_user_not_found(async_client):
    form_data = {
        "username": "nonexistentuser@here.edu",
        "password": "DoesNotMatter123!"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_incorrect_password(async_client, verified_user):
    form_data = {
        "username": verified_user.email,
        "password": "IncorrectPassword123!"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 307
    assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_unverified_user(async_client, unverified_user):
    form_data = {
        "username": unverified_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 307

@pytest.mark.asyncio
async def test_login_locked_user(async_client, locked_user):
    form_data = {
        "username": locked_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 307
    assert "Account locked due to too many failed login attempts." in response.json().get("detail", "")
@pytest.mark.asyncio
async def test_delete_user_does_not_exist(async_client, admin_token):
    non_existent_user_id = "00000000-0000-0000-0000-000000000000"  # Valid UUID format
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(f"/users/{non_existent_user_id}", headers=headers)
    assert delete_response.status_code == 404

@pytest.mark.asyncio
async def test_update_user_github(async_client, admin_user, admin_token):
    updated_data = {"github_profile_url": "http://www.github.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["github_profile_url"] == updated_data["github_profile_url"]

@pytest.mark.asyncio
async def test_update_user_linkedin(async_client, admin_user, admin_token):
    updated_data = {"linkedin_profile_url": "http://www.linkedin.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["linkedin_profile_url"] == updated_data["linkedin_profile_url"]

@pytest.mark.asyncio
async def test_list_users_as_admin(async_client, admin_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert 'items' in response.json()

@pytest.mark.asyncio
async def test_list_users_as_manager(async_client, manager_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {manager_token}"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_list_users_unauthorized(async_client, user_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403  # Forbidden, as expected for regular user

@pytest.mark.asyncio
async def test_update_user_invalid_data(async_client, admin_user, admin_token):
    """Test updating user with invalid data"""
    invalid_data = {"email": "not-an-email"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(
        f"/users/{admin_user.id}",
        json=invalid_data,
        headers=headers
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_update_nonexistent_user(async_client, admin_token):
    """Test updating a user that doesn't exist"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(
        f"/users/nonexistent-id",
        json={"first_name": "Test"},
        headers=headers
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_delete_user_unauthorized(async_client, user_token, admin_user):
    """Test deleting user without proper authorization"""
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.delete(
        f"/users/{admin_user.id}",
        headers=headers
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_nonexistent_user(async_client, admin_token_headers):  # Changed to admin token
    response = await async_client.put(
        "/users/99999",
        headers=admin_token_headers,
        json={"nickname": "new_nickname"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_delete_user(async_client, admin_token_headers, test_user):
    response = await async_client.delete(
        f"/users/{test_user.id}",
        headers=admin_token_headers
    )
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_get_user_me(async_client, normal_user_token_headers, test_user):
    response = await async_client.get(
        "/users/me", 
        headers=normal_user_token_headers
    )
    assert response.status_code == 200
    assert response.json()["email"] == test_user.email

@pytest.mark.asyncio
async def test_update_user_validation_error(async_client, normal_user_token_headers):
    response = await async_client.patch(
        "/users/me",
        headers=normal_user_token_headers,
        json={"email": "invalid_email"}
    )
    assert response.status_code == 405

@pytest.mark.asyncio
async def test_get_user_not_found(async_client, admin_token):
    """Test getting a non-existent user"""
    non_existent_id = uuid4()
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(f"/users/{non_existent_id}", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_update_user_no_changes(async_client, admin_user, admin_token):
    """Test updating a user with empty data"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(
        f"/users/{admin_user.id}",
        json={},
        headers=headers
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_user_invalid_data(async_client, admin_token):
    """Test creating a user with invalid data"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    invalid_user_data = {
        "email": "not-an-email",
        "password": "short"
    }
    response = await async_client.post(
        "/users/",
        json=invalid_user_data,
        headers=headers
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_list_users_invalid_pagination(async_client, admin_token):
    """Test listing users with invalid pagination parameters"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(
        "/users/?skip=-1&limit=0",
        headers=headers
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_verify_email_invalid_token(async_client):
    """Test email verification with invalid token"""
    user_id = uuid4()
    response = await async_client.get(f"/verify-email/{user_id}/invalid-token")
    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid or expired verification token"

@pytest.mark.asyncio
async def test_get_current_user_not_found(async_client, normal_user_token_headers):
    """Test getting current user when user doesn't exist in DB"""
    response = await async_client.get("/users/me", headers=normal_user_token_headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_update_current_user_success(async_client, normal_user_token_headers):
    """Test successful update of current user"""
    update_data = {
        "first_name": "Updated",
        "last_name": "User"
    }
    response = await async_client.patch(
        "/users/me",
        headers=normal_user_token_headers,
        json=update_data
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == update_data["first_name"]
    assert response.json()["last_name"] == update_data["last_name"]

@pytest.mark.asyncio
async def test_register_user_success(async_client):
    """Test successful user registration"""
    user_data = {
        "email": "newuser@example.com",
        "password": "ValidPassword123!",
        "nickname": "newuser123"
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]

@pytest.mark.asyncio
async def test_login_missing_credentials(async_client):
    """Test login attempt with missing credentials"""
    form_data = {
        "username": "",
        "password": ""
    }
    response = await async_client.post(
        "/login/",
        data=urlencode(form_data),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_update_user_server_error(async_client, admin_token, monkeypatch):
    """Test handling of server error during user update"""
    async def mock_update(*args, **kwargs):
        return None
    
    from app.services.user_service import UserService
    monkeypatch.setattr(UserService, "update", mock_update)
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(
        f"/users/{uuid4()}",
        json={"email": "test@example.com"},
        headers=headers
    )
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_user_server_error(async_client, admin_token, monkeypatch):
    """Test handling of server error during user creation"""
    async def mock_create(*args, **kwargs):
        return None
    
    from app.services.user_service import UserService
    monkeypatch.setattr(UserService, "create", mock_create)
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "password": "ValidPassword123!",
            "nickname": "testuser"
        },
        headers=headers
    )
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to create user"

@pytest.mark.asyncio
async def test_delete_user_unauthorized_different_user(async_client, normal_user_token_headers, admin_user):
    """Test deleting a different user's account"""
    response = await async_client.delete(
        f"/users/{admin_user.id}",
        headers=normal_user_token_headers
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to delete this user"

@pytest.mark.asyncio
async def test_update_current_user_validation_error(async_client, normal_user_token_headers):
    """Test updating current user with invalid data"""
    invalid_data = {
        "email": "not-an-email",
        "nickname": "!@#$%^"  # Invalid nickname format
    }
    response = await async_client.patch(
        "/users/me",
        headers=normal_user_token_headers,
        json=invalid_data
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_list_users_pagination(async_client, admin_token):
    """Test user listing with pagination"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Test first page
    response = await async_client.get("/users/?skip=0&limit=5", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert "links" in data
    
    # Test second page
    response = await async_client.get("/users/?skip=5&limit=5", headers=headers)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_register_user_duplicate_email_different_case(async_client, verified_user):
    """Test registration with existing email in different case"""
    user_data = {
        "email": verified_user.email.upper(),  # Use uppercase version of existing email
        "password": "ValidPassword123!",
        "nickname": "newuser123"
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 400
    assert "Email already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_verify_email_success(async_client, unverified_user):
    """Test successful email verification"""
    response = await async_client.get(
        f"/verify-email/{unverified_user.id}/{unverified_user.verification_token}"
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Email verified successfully"

@pytest.mark.asyncio
async def test_update_user_not_found(async_client, admin_token):
    """Test updating a non-existent user"""
    non_existent_id = uuid4()
    headers = {"Authorization": f"Bearer {admin_token}"}
    update_data = {"first_name": "New Name"}
    
    response = await async_client.put(
        f"/users/{non_existent_id}",
        headers=headers,
        json=update_data
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_create_user_with_existing_nickname(async_client, admin_token, verified_user):
    """Test creating a user with an existing nickname"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    user_data = {
        "email": "new.user@example.com",
        "password": "ValidPassword123!",
        "nickname": verified_user.nickname  # Use existing nickname
    }
    response = await async_client.post("/users/", json=user_data, headers=headers)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_update_current_user_not_found(async_client, normal_user_token_headers, monkeypatch):
    """Test updating current user when user no longer exists"""
    async def mock_get_by_id(*args, **kwargs):
        return None
    
    from app.services.user_service import UserService
    monkeypatch.setattr(UserService, "get_by_id", mock_get_by_id)
    
    response = await async_client.patch(
        "/users/me",
        headers=normal_user_token_headers,
        json={"first_name": "Updated"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_list_users_empty_db(async_client, admin_token, monkeypatch):
    """Test listing users when database is empty"""
    async def mock_list_users(*args, **kwargs):
        return []
    
    async def mock_count(*args, **kwargs):
        return 0
    
    from app.services.user_service import UserService
    monkeypatch.setattr(UserService, "list_users", mock_list_users)
    monkeypatch.setattr(UserService, "count", mock_count)
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get("/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0
    assert data["total"] == 0

@pytest.mark.asyncio
async def test_register_user_with_invalid_password(async_client):
    """Test registration with invalid password format"""
    user_data = {
        "email": "newuser@example.com",
        "password": "weak",  # Invalid password
        "nickname": "newuser123"
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_update_user_with_invalid_url(async_client, admin_token, admin_user):
    """Test updating user with invalid URL format"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    invalid_data = {
        "profile_picture_url": "not-a-url",
        "github_profile_url": "invalid-github-url",
        "linkedin_profile_url": "invalid-linkedin-url"
    }
    response = await async_client.put(
        f"/users/{admin_user.id}",
        headers=headers,
        json=invalid_data
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_user_missing_fields(async_client, admin_token):
    """Test creating a user with missing required fields"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    incomplete_user_data = {
        "email": "newuser@example.com"
        # Missing password and nickname
    }
    response = await async_client.post(
        "/users/",
        json=incomplete_user_data,
        headers=headers
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_delete_user_not_found(async_client, admin_token):
    """Test deleting a user that does not exist"""
    non_existent_user_id = uuid4()
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.delete(f"/users/{non_existent_user_id}", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_get_user_unauthorized(async_client):
    """Test accessing user details without authorization"""
    user_id = uuid4()
    response = await async_client.get(f"/users/{user_id}")
    assert response.status_code == 401  # Unauthorized

@pytest.mark.asyncio
async def test_update_user_unauthorized(async_client, admin_user):
    """Test updating a user without authorization"""
    update_data = {"first_name": "Unauthorized"}
    response = await async_client.put(f"/users/{admin_user.id}", json=update_data)
    assert response.status_code == 401  # Unauthorized

@pytest.mark.asyncio
async def test_delete_user_unauthorized(async_client, admin_user):
    """Test deleting a user without authorization"""
    response = await async_client.delete(f"/users/{admin_user.id}")
    assert response.status_code == 401  # Unauthorized

@pytest.mark.asyncio
async def test_register_user_existing_email(async_client, verified_user):
    """Test registration with an email that already exists"""
    user_data = {
        "email": verified_user.email,
        "password": "AnotherValidPassword123!",
        "nickname": "unique_nickname"
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 400
    assert "Email already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_locked_user(async_client, locked_user):
    """Test login attempt with a locked user account"""
    form_data = {
        "username": locked_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 400
    assert "Account locked due to too many failed login attempts." in response.json()["detail"]

@pytest.mark.asyncio
async def test_update_user_invalid_role(async_client, admin_user, admin_token):
    """Test updating a user with an invalid role"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    invalid_role_data = {"role": "INVALID_ROLE"}
    response = await async_client.put(
        f"/users/{admin_user.id}",
        json=invalid_role_data,
        headers=headers
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_user_invalid_uuid(async_client, admin_token):
    """Test getting a user with an invalid UUID format"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get("/users/invalid-uuid", headers=headers)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_update_user_invalid_uuid(async_client, admin_token):
    """Test updating a user with an invalid UUID format"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(
        "/users/invalid-uuid",
        json={"first_name": "Test"},
        headers=headers
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_list_users_with_search(async_client, admin_token, users_with_same_role_50_users):
    """Test listing users with search parameters"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Test search by email
    response = await async_client.get(
        "/users/?search=example.com",
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0

@pytest.mark.asyncio
async def test_list_users_with_role_filter(async_client, admin_token, verified_user):
    """Test listing users with role filter"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(
        "/users/?role=AUTHENTICATED",
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert all(user["role"] == "AUTHENTICATED" for user in data["items"])

@pytest.mark.asyncio
async def test_update_user_partial_data(async_client, admin_token, admin_user):
    """Test updating user with partial data"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    update_data = {
        "first_name": "UpdatedFirst",
        # Omitting other fields
    }
    response = await async_client.put(
        f"/users/{admin_user.id}",
        json=update_data,
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "UpdatedFirst"

@pytest.mark.asyncio
async def test_update_current_user_server_error(async_client, normal_user_token_headers, monkeypatch):
    """Test server error during current user update"""
    async def mock_update(*args, **kwargs):
        raise Exception("Database error")
    
    from app.services.user_service import UserService
    monkeypatch.setattr(UserService, "update", mock_update)
    
    response = await async_client.patch(
        "/users/me",
        headers=normal_user_token_headers,
        json={"first_name": "NewName"}
    )
    assert response.status_code == 500

@pytest.mark.asyncio
async def test_verify_email_invalid_user_id(async_client):
    """Test email verification with invalid user ID format"""
    response = await async_client.get("/verify-email/invalid-uuid/some-token")
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_register_user_service_error(async_client, monkeypatch):
    """Test registration when user service fails"""
    async def mock_register(*args, **kwargs):
        return None
    
    from app.services.user_service import UserService
    monkeypatch.setattr(UserService, "register_user", mock_register)
    
    user_data = {
        "email": "new@example.com",
        "password": "ValidPassword123!",
        "nickname": "newuser"
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_login_with_non_dict_user(async_client, monkeypatch):
    """Test login when user service returns non-dict user"""
    class MockUser:
        email = "test@example.com"
        role = UserRole.AUTHENTICATED
        
    async def mock_login(*args, **kwargs):
        return MockUser()
    
    from app.services.user_service import UserService
    monkeypatch.setattr(UserService, "login_user", mock_login)
    
    form_data = {
        "username": "test@example.com",
        "password": "password123"
    }
    response = await async_client.post(
        "/login/",
        data=urlencode(form_data),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_current_user_validation_error(async_client, normal_user_token_headers, monkeypatch):
    """Test getting current user with validation error"""
    class InvalidUser:
        def __dict__(self):
            return {"invalid": "data"}
    
    async def mock_get_by_id(*args, **kwargs):
        return InvalidUser()
    
    from app.services.user_service import UserService
    monkeypatch.setattr(UserService, "get_by_id", mock_get_by_id)
    
    response = await async_client.get("/users/me", headers=normal_user_token_headers)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_update_user_with_empty_body(async_client, admin_token, admin_user):
    """Test updating user with empty request body"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(
        f"/users/{admin_user.id}",
        json={},
        headers=headers
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_list_users_service_error(async_client, admin_token, monkeypatch):
    """Test listing users when service throws an error"""
    async def mock_list_users(*args, **kwargs):
        raise Exception("Database error")
    
    from app.services.user_service import UserService
    monkeypatch.setattr(UserService, "list_users", mock_list_users)
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get("/users/", headers=headers)
    assert response.status_code == 500

@pytest.mark.asyncio
async def test_get_me_with_invalid_token(async_client):
    """Test accessing /me endpoint with invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = await async_client.get("/me", headers=headers)
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_me_success(async_client, verified_user, user_token):
    """Test successful retrieval of current user information"""
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.get("/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == verified_user.email
    assert "links" in data  # Verify HATEOAS links are present

@pytest.mark.asyncio
async def test_update_me_validation(async_client, user_token):
    """Test /me update endpoint with invalid data"""
    headers = {"Authorization": f"Bearer {user_token}"}
    invalid_data = {
        "email": "not-an-email",
        "profile_picture_url": "not-a-url"
    }
    response = await async_client.patch("/me", json=invalid_data, headers=headers)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_user_email_service_failure(async_client, admin_token, monkeypatch):
    """Test user creation when email service fails"""
    async def mock_send_email(*args, **kwargs):
        raise Exception("Email service failure")
    
    from app.services.email_service import EmailService
    monkeypatch.setattr(EmailService, "send_verification_email", mock_send_email)
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    user_data = {
        "email": "new@example.com",
        "password": "ValidPassword123!",
        "nickname": "newuser"
    }
    response = await async_client.post("/users/", json=user_data, headers=headers)
    assert response.status_code == 500
    assert "Failed to create user" in response.json()["detail"]

@pytest.mark.asyncio
async def test_role_inheritance_access(async_client, admin_token):
    """Test role inheritance for access control"""
    # Admin should have access to manager-only endpoints
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get("/users/", headers=headers)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_user_response_model(async_client, admin_token, admin_user):
    """Test update user response model structure"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    update_data = {"first_name": "Updated"}
    response = await async_client.put(
        f"/users/{admin_user.id}",
        json=update_data,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    # Verify all required fields are present
    required_fields = ["id", "email", "nickname", "role", "created_at", "updated_at", "links"]
    assert all(field in data for field in required_fields)
    # Verify HATEOAS links
    assert "self" in data["links"]
    assert "delete" in data["links"]
    assert "update" in data["links"]

@pytest.mark.asyncio
async def test_verify_email_expired_token(async_client, unverified_user, monkeypatch):
    """Test email verification with expired token"""
    async def mock_verify(*args, **kwargs):
        return False
    
    from app.services.user_service import UserService
    monkeypatch.setattr(UserService, "verify_email_with_token", mock_verify)
    
    response = await async_client.get(
        f"/verify-email/{unverified_user.id}/expired_token"
    )
    assert response.status_code == 400
    assert "Invalid or expired verification token" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_user_with_role(async_client, admin_token):
    """Test creating user with specific role"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    user_data = {
        "email": "manager@example.com",
        "password": "ValidPassword123!",
        "nickname": "manager",
        "role": "MANAGER"
    }
    response = await async_client.post("/users/", json=user_data, headers=headers)
    assert response.status_code == 201
    assert response.json()["role"] == "MANAGER"

@pytest.mark.asyncio
async def test_list_users_invalid_role(async_client, admin_token):
    """Test listing users with invalid role filter"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get("/users/?role=INVALID_ROLE", headers=headers)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_list_users_negative_skip(async_client, admin_token):
    """Test listing users with negative skip value"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get("/users/?skip=-1", headers=headers)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_update_user_empty_update(async_client, admin_token, admin_user):
    """Test updating user with empty update data"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(
        f"/users/{admin_user.id}",
        json={},
        headers=headers
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_user_invalid_email_format(async_client, admin_token):
    """Test creating user with invalid email format"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    user_data = {
        "email": "invalid-email",
        "password": "ValidPassword123!",
        "nickname": "testuser"
    }
    response = await async_client.post("/users/", json=user_data, headers=headers)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_update_me_invalid_fields(async_client, user_token):
    """Test updating current user with invalid fields"""
    headers = {"Authorization": f"Bearer {user_token}"}
    invalid_data = {
        "invalid_field": "value",
        "another_invalid": "value"
    }
    response = await async_client.patch("/me", json=invalid_data, headers=headers)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_register_missing_required_fields(async_client):
    """Test registration with missing required fields"""
    user_data = {
        "email": "test@example.com"
        # Missing password
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_verify_hateoas_links(async_client, admin_token, admin_user):
    """Test HATEOAS links in user response"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "links" in data
    assert any(link["rel"] == "self" for link in data["links"])
    assert any(link["rel"] == "update" for link in data["links"])
    assert any(link["rel"] == "delete" for link in data["links"])

@pytest.mark.asyncio
async def test_list_users_pagination_links(async_client, admin_token, users_with_same_role_50_users):
    """Test pagination links in list users response"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get("/users/?limit=10", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "links" in data
    assert any(link["rel"] == "next" for link in data["links"])
    assert any(link["rel"] == "self" for link in data["links"])

@pytest.mark.asyncio
async def test_register_user_service_failure(async_client, monkeypatch):
    """Test registration when user service fails unexpectedly"""
    async def mock_register(*args, **kwargs):
        raise Exception("Database error")
    
    from app.services.user_service import UserService
    monkeypatch.setattr(UserService, "register_user", mock_register)
    
    user_data = {
        "email": "test@example.com",
        "password": "ValidPassword123!"
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 500
    assert "Failed to register user" in response.json()["detail"]

@pytest.mark.asyncio
async def test_me_endpoint_no_user(async_client, user_token, monkeypatch):
    """Test /me endpoint when user not found in database"""
    async def mock_get_current_user(*args, **kwargs):
        return None
    
    from app.dependencies import get_current_user
    monkeypatch.setattr("app.dependencies.get_current_user", mock_get_current_user)
    
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.get("/me", headers=headers)
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_update_me_database_error(async_client, user_token, monkeypatch):
    """Test updating current user when database operation fails"""
    async def mock_update(*args, **kwargs):
        raise Exception("Database error")
    
    from app.services.user_service import UserService
    monkeypatch.setattr(UserService, "update", mock_update)
    
    headers = {"Authorization": f"Bearer {user_token}"}
    update_data = {"first_name": "NewName"}
    response = await async_client.patch("/me", json=update_data, headers=headers)
    assert response.status_code == 500
    assert "Internal server error" in response.json()["detail"]

@pytest.mark.asyncio
async def test_list_users_zero_limit(async_client, admin_token):
    """Test listing users with zero limit"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get("/users/?limit=0", headers=headers)
    assert response.status_code == 422
    assert "Limit must be greater than 0" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_user_email_service_error(async_client, admin_token, monkeypatch):
    """Test user creation when email service fails"""
    async def mock_send_email(*args, **kwargs):
        raise Exception("Email service error")
    
    from app.services.email_service import EmailService
    monkeypatch.setattr(EmailService, "send_verification_email", mock_send_email)
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    user_data = {
        "email": "new@example.com",
        "password": "ValidPassword123!",
        "nickname": "newuser"
    }
    response = await async_client.post("/users/", json=user_data, headers=headers)
    assert response.status_code == 500
    assert "Failed to create user" in response.json()["detail"]

@pytest.mark.asyncio
async def test_update_user_validation_error(async_client, admin_token, admin_user, monkeypatch):
    """Test user update with validation error"""
    async def mock_update(*args, **kwargs):
        raise ValidationError("Invalid data")
    
    from app.services.user_service import UserService
    monkeypatch.setattr(UserService, "update", mock_update)
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    update_data = {"email": "newemail@example.com"}
    response = await async_client.put(f"/users/{admin_user.id}", json=update_data, headers=headers)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_list_users_count_error(async_client, admin_token, monkeypatch):
    """Test list users when count operation fails"""
    async def mock_count(*args, **kwargs):
        raise Exception("Database error")
    
    from app.services.user_service import UserService
    monkeypatch.setattr(UserService, "count", mock_count)
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get("/users/", headers=headers)
    assert response.status_code == 500
    assert "Failed to retrieve users" in response.json()["detail"]

@pytest.mark.asyncio
async def test_register_validation_error(async_client):
    """Test registration with data that fails model validation"""
    user_data = {
        "email": "test@example.com",
        "password": "short"  # Too short password
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_user_response_model_validation(async_client, admin_token, admin_user):
    """Test response model validation for user endpoints"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    
    # Verify model structure
    assert isinstance(data["id"], str)
    assert isinstance(data["email"], str)
    assert isinstance(data["created_at"], str)
    assert isinstance(data["links"], list)

@pytest.mark.asyncio
async def test_list_users_model_validation(async_client, admin_token):
    """Test list users response model validation"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get("/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    
    # Verify pagination model structure
    assert "total" in data
    assert "items" in data
    assert "links" in data
    assert isinstance(data["items"], list)
    assert isinstance(data["total"], int)

@pytest.mark.asyncio
async def test_update_me_model_validation_error(async_client, user_token):
    """Test update current user with invalid model data"""
    headers = {"Authorization": f"Bearer {user_token}"}
    invalid_data = {
        "email": "not-an-email",
        "role": "INVALID_ROLE"  # Invalid enum value
    }
    response = await async_client.patch("/me", json=invalid_data, headers=headers)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

@pytest.mark.asyncio
async def test_create_user_model_construction_error(async_client, admin_token, monkeypatch):
    """Test user creation when model construction fails"""
    async def mock_model_validate(*args, **kwargs):
        raise ValidationError("Model validation failed")
    
    from app.schemas.user_schemas import UserResponse
    monkeypatch.setattr(UserResponse, "model_validate", mock_model_validate)
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    user_data = {
        "email": "test@example.com",
        "password": "ValidPassword123!"
    }
    response = await async_client.post("/users/", json=user_data, headers=headers)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_user_link_generation_error(async_client, admin_token, admin_user, monkeypatch):
    """Test user retrieval when link generation fails"""
    def mock_create_links(*args, **kwargs):
        raise Exception("Link generation failed")
    
    from app.utils.link_generation import create_user_links
    monkeypatch.setattr("app.utils.link_generation.create_user_links", mock_create_links)
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert response.status_code == 500

@pytest.mark.asyncio
async def test_list_users_empty_result(async_client, admin_token, monkeypatch):
    """Test listing users when query returns empty result"""
    async def mock_list_users(*args, **kwargs):
        return []
    
    from app.services.user_service import UserService
    monkeypatch.setattr(UserService, "list_users", mock_list_users)
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get("/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0
    assert data["total"] == 0

@pytest.mark.asyncio
async def test_update_user_model_construction_error(async_client, admin_token, admin_user, monkeypatch):
    """Test user update when response model construction fails"""
    async def mock_update(*args, **kwargs):
        class InvalidUser:
            def __dict__(self):
                return {"invalid": "data"}
        return InvalidUser()
    
    from app.services.user_service import UserService
    monkeypatch.setattr(UserService, "update", mock_update)
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    update_data = {"first_name": "Updated"}
    response = await async_client.put(f"/users/{admin_user.id}", json=update_data, headers=headers)
    assert response.status_code == 422



