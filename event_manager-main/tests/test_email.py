import pytest
from unittest.mock import MagicMock, patch
from app.services.email_service import EmailService

@pytest.mark.asyncio
async def test_send_markdown_email(email_service, mocker):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }
    
    # Create a mock for smtp_client
    mock_smtp = MagicMock()
    email_service.smtp_client = mock_smtp
    
    # Test email sending
    await email_service.send_user_email(user_data, 'email_verification')
    
    # Verify that send_email was called once
    assert mock_smtp.send_email.call_count == 1
