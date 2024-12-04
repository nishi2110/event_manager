from typing import Optional
import re

def validate_nickname(nickname: str) -> tuple[bool, Optional[str]]:
    """
    Validates a nickname according to the following rules:
    - Length between 3 and 30 characters
    - Only alphanumeric characters, underscores, and hyphens
    - Cannot start or end with special characters
    - No consecutive special characters
    - Not in reserved word list
    
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    # Reserved words that cannot be used as nicknames
    RESERVED_WORDS = {'admin', 'moderator', 'system', 'anonymous', 'user', 
                     'support', 'help', 'info', 'administrator', 'mod'}
    
    # Check length
    if len(nickname) < 3:
        return False, "Nickname must be at least 3 characters long"
    if len(nickname) > 30:
        return False, "Nickname cannot exceed 30 characters"
    
    # Check if nickname is in reserved words
    if nickname.lower() in RESERVED_WORDS:
        return False, "This nickname is reserved and cannot be used"
    
    # Check for valid characters and pattern
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_-]*[a-zA-Z0-9]$', nickname):
        return False, "Nickname must start and end with alphanumeric characters and contain only letters, numbers, underscores, and hyphens"
    
    # Check for consecutive special characters
    if re.search(r'[_-]{2,}', nickname):
        return False, "Nickname cannot contain consecutive special characters"
    
    return True, None 

def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """
    Validates a password according to security best practices:
    - Minimum length of 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    - Maximum length of 128 characters
    
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not password:
        return False, "Password cannot be empty"
        
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
        
    if len(password) > 128:
        return False, "Password cannot exceed 128 characters"
        
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
        
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
        
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
        
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        return False, "Password must contain at least one special character"
    
    return True, None 