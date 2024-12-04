import pytest
from settings.config import Settings
from app.dependencies import get_settings,get_db,get_email_service,get_current_user,require_role
from app.services.email_service import EmailService
from app.utils.template_manager import TemplateManager
from unittest.mock import MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.jwt_service import decode_token
from fastapi.testclient import TestClient
from fastapi import HTTPException

def test_get_settings():
    settings = get_settings()
    assert isinstance(settings, Settings)

def test_get_email_service(mocker):
    mock_template_manager = mocker.patch.object(TemplateManager, '__init__', return_value=None)
    email_service = get_email_service()
    assert isinstance(email_service, EmailService)
    mock_template_manager.assert_called_once()


async def test_get_db(mocker):
    # Mock the session factory and session
    mock_session_factory = MagicMock()
    mock_session = MagicMock(AsyncSession)
    mock_session_factory.return_value.__aenter__.return_value = mock_session
    mocker.patch('app.database.Database.get_session_factory', return_value=mock_session_factory)

    # Run the function and get the session
    async for session in get_db():
        # Verify that the session returned is the mock session
        assert session is mock_session

@pytest.mark.asyncio
async def test_get_current_user(mocker):
    mock_decode_token = mocker.patch('app.dependencies.decode_token', return_value={'sub': 'user_id', 'role': 'admin'})
    token = 'dummy_token'
    
    user = get_current_user(token=token)
    
    assert user['user_id'] == 'user_id'
    assert user['role'] == 'admin'
    mock_decode_token.assert_called_once_with(token)
    
    # Test invalid token (when decode_token returns None)
    mock_decode_token.return_value = None
    with pytest.raises(HTTPException):
        await get_current_user(token=token)

@pytest.mark.asyncio
async def test_require_role(mocker):
    # Test valid role
    role_checker = require_role('admin')
    result = role_checker(current_user={'user_id': 'user_id', 'role': 'admin'})
    assert result['role'] == 'admin'

    # Test invalid role
    with pytest.raises(HTTPException):
        role_checker(current_user={'user_id': 'user_id', 'role': 'user'})
