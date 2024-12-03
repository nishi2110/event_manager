# test_users.py

from builtins import len
import pytest
from httpx import AsyncClient
from sqlalchemy.future import select
from faker import Faker
from uuid import uuid4

from app.models.user_model import User, UserRole
from app.utils.security import verify_password

@pytest.mark.asyncio
async def test_user_creation(db_session, verified_user):
    """Test that a user is correctly created and stored in the database."""
    result = await db_session.execute(select(User).filter_by(email=verified_user.email))
    stored_user = result.scalars().first()
    assert stored_user is not None
    assert stored_user.email == verified_user.email
    assert verify_password("MySuperPassword$1234", stored_user.hashed_password)

# Apply similar corrections to other test functions
@pytest.mark.asyncio
async def test_locked_user(db_session, locked_user):
    result = await db_session.execute(select(User).filter_by(email=locked_user.email))
    stored_user = result.scalars().first()
    assert stored_user.is_locked

@pytest.mark.asyncio
async def test_verified_user(db_session, verified_user):
    result = await db_session.execute(select(User).filter_by(email=verified_user.email))
    stored_user = result.scalars().first()
    assert stored_user.email_verified

@pytest.mark.asyncio
async def test_user_role(db_session, admin_user):
    result = await db_session.execute(select(User).filter_by(email=admin_user.email))
    stored_user = result.scalars().first()
    assert stored_user.role == UserRole.ADMIN

@pytest.mark.asyncio
async def test_bulk_user_creation_performance():
    faker = Faker()
    
    # Create users with unique nicknames using random suffixes
    users_data = [
        {
            "id": uuid4(),
            "nickname": f"{faker.user_name()}_{uuid4().hex[:8]}",  # Add random suffix
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "role": "AUTHENTICATED",
            "is_professional": False,
            "is_locked": False,
            "password_hash": f"{faker.password(length=10)}"
        }
        for _ in range(300)
    ]

    # ... rest of your test code ...

@pytest.mark.asyncio
async def test_password_hashing(user):
    assert verify_password("MySuperPassword$1234", user.hashed_password)

@pytest.mark.asyncio
async def test_user_unlock(db_session, locked_user):
    locked_user.unlock_account()
    await db_session.commit()
    result = await db_session.execute(select(User).filter_by(email=locked_user.email))
    updated_user = result.scalars().first()
    assert not updated_user.is_locked

@pytest.mark.asyncio
async def test_update_professional_status(db_session, verified_user):
    verified_user.update_professional_status(True)
    await db_session.commit()
    result = await db_session.execute(select(User).filter_by(email=verified_user.email))
    updated_user = result.scalars().first()
    assert updated_user.is_professional
    assert updated_user.professional_status_updated_at is not None