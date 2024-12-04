# tests/test_utils/test_common.py

import pytest
from pydantic import ValidationError
from datetime import datetime
from app.utils.common import format_datetime, validate_url, sanitize_input, generate_random_string

def test_format_datetime():
    """Test datetime formatting function"""
    # Test valid datetime
    test_date = datetime(2024, 1, 1, 12, 0, 0)
    assert format_datetime(test_date) == "2024-01-01 12:00:00"
    
    # Test invalid input
    with pytest.raises(ValueError):
        format_datetime("not a datetime")

def test_validate_url():
    """Test URL validation function"""
    valid_urls = [
        "https://example.com",
        "http://test.com/path",
        "https://sub.domain.com/path?query=1"
    ]
    invalid_urls = [
        "not_a_url",
        "ftp://invalid.com",
        "http:/missing-slash.com",
        None,
        ""
    ]
    
    for url in valid_urls:
        assert validate_url(url) is True
        
    for url in invalid_urls:
        assert validate_url(url) is False

def test_sanitize_input():
    """Test input sanitization function"""
    test_cases = [
        ("<script>alert('xss')</script>", "alert('xss')"),
        ("Normal text", "Normal text"),
        ("Text with <b>tags</b>", "Text with tags"),
        ("<a href='http://evil.com'>click</a>", "click"),
        ("", ""),
        (None, "")
    ]
    
    for input_text, expected in test_cases:
        result = sanitize_input(input_text)
        assert result == expected, f"Failed for input: {input_text}, got: {result}, expected: {expected}"

def test_generate_random_string():
    """Test random string generation"""
    # Test default length
    assert len(generate_random_string()) == 10
    
    # Test custom length
    assert len(generate_random_string(15)) == 15
    
    # Test uniqueness
    strings = [generate_random_string(8) for _ in range(100)]
    assert len(set(strings)) == len(strings)
    
    # Test invalid length
    with pytest.raises(ValueError):
        generate_random_string(-1)
    
    with pytest.raises(ValueError):
        generate_random_string(0)