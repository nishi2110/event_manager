import pytest
from pathlib import Path
from app.utils.template_manager import TemplateManager

@pytest.fixture
def template_manager():
    return TemplateManager()

def test_template_loading(template_manager, tmp_path):
    """Test template loading functionality"""
    # Create test template
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    template_file = template_dir / "test.html"
    template_file.write_text("Hello {{name}}!")
    
    # Set template dir
    template_manager.templates_dir = template_dir
    
    # Test loading
    content = template_manager.render_template("test", name="World")
    assert "Hello World!" in content

def test_template_not_found(template_manager):
    """Test handling of missing templates"""
    with pytest.raises(FileNotFoundError):
        template_manager.render_template("nonexistent")

def test_template_variables(template_manager, tmp_path):
    """Test template variable rendering"""
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    template_file = template_dir / "vars.html"
    template_file.write_text("{{var1}} {{var2}}")
    
    template_manager.templates_dir = template_dir
    result = template_manager.render_template("vars", var1="Hello", var2="World")
    assert result == "Hello World"

def test_email_style_application(template_manager):
    """Test email styling functionality"""
    html = "<p>Test</p>"
    styled = template_manager._apply_email_styles(html)
    assert "font-family" in styled
    assert "color" in styled 