import pytest
from backend.utils.json_parser import (
    extract_json_from_markdown,
    extract_json_from_response,
    extract_json_list_from_response,
)

class TestExtractJsonFromMarkdown:
    def test_returns_none_for_empty_string(self):
        assert extract_json_from_markdown("") is None

    def test_returns_none_for_none(self):
        assert extract_json_from_markdown(None) is None

    def test_returns_none_for_non_string(self):
        assert extract_json_from_markdown(123) is None

    def test_plain_json_object(self):
        text = '{"name": "Alice"}'
        assert extract_json_from_markdown(text) == {"name": "Alice"}

    def test_plain_json_array(self):
        text = '[1, 2, 3]'
        assert extract_json_from_markdown(text) == [1, 2, 3]

    def test_json_in_json_code_fence(self):
        text = 'Here is the result:\n```json\n{"key": "value"}\n```\nDone.'
        assert extract_json_from_markdown(text) == {"key": "value"}

    def test_json_in_generic_code_fence(self):
        text = 'Result:\n```\n{"foo": 42}\n```'
        assert extract_json_from_markdown(text) == {"foo": 42}

    def test_json_with_surrounding_text(self):
        text = 'Based on the analysis, I found: {"score": 0.95, "tier": "high"} which is great.'
        result = extract_json_from_markdown(text)
        assert result == {"score": 0.95, "tier": "high"}

    def test_invalid_json_returns_none(self):
        text = '```json\n{invalid json}\n```'
        assert extract_json_from_markdown(text) is None

    def test_nested_json(self):
        text = '{"users": [{"id": 1, "name": "Bob"}]}'
        assert extract_json_from_markdown(text) == {"users": [{"id": 1, "name": "Bob"}]}

    def test_multiline_code_fence(self):
        text = '''Some text before
```json
{
  "status": "ok",
  "count": 5
}
```
Some text after'''
        result = extract_json_from_markdown(text)
        assert result == {"status": "ok", "count": 5}


class TestExtractJsonFromResponse:
    def test_returns_dict(self):
        text = '```json\n{"score": 0.8}\n```'
        assert extract_json_from_response(text) == {"score": 0.8}

    def test_returns_none_for_list(self):
        text = '[1, 2, 3]'
        assert extract_json_from_response(text) is None

    def test_returns_none_for_invalid(self):
        text = 'no json here'
        assert extract_json_from_response(text) is None


class TestExtractJsonListFromResponse:
    def test_returns_list(self):
        text = '```json\n[1, 2, 3]\n```'
        assert extract_json_list_from_response(text) == [1, 2, 3]

    def test_returns_none_for_dict(self):
        text = '{"key": "value"}'
        assert extract_json_list_from_response(text) is None

    def test_returns_none_for_invalid(self):
        text = 'not json'
        assert extract_json_list_from_response(text) is None
