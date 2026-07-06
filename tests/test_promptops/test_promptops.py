import pytest
from backend.promptops.models import PromptVersion
from backend.promptops.manager import prompt_manager
from backend.promptops.renderer import prompt_renderer

def test_prompt_version_creation_and_activation(db_session):
    # Override SessionLocal to use test db_session
    import backend.promptops.manager as manager
    manager.SessionLocal = lambda: db_session

    version_id = prompt_manager.create_version(
        prompt_name="test_prompt",
        content="Hello {{name}}!",
        variables=["name"],
        author="tester"
    )
    assert version_id is not None

    # Retrieve and activate
    prompt_manager.activate_version("test_prompt", version_id)
    active = prompt_manager.get_active_prompt("test_prompt")
    assert active is not None
    assert active.id == version_id
    assert active.content == "Hello {{name}}!"

def test_prompt_rendering(db_session):
    # Override SessionLocal to use test db_session
    import backend.promptops.manager as manager
    manager.SessionLocal = lambda: db_session

    version_id = prompt_manager.create_version(
        prompt_name="hello_prompt",
        content="Hello {{name}}!",
        variables=["name"],
        author="tester"
    )
    prompt_manager.activate_version("hello_prompt", version_id)

    # Success render
    rendered = prompt_renderer.render("hello_prompt", name="World")
    assert rendered == "Hello World!"

    # Fail render (missing variable)
    with pytest.raises(ValueError) as exc:
        prompt_renderer.render("hello_prompt")
    assert "Missing required variable 'name'" in str(exc.value)
