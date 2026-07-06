import json
import re
import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)

def extract_json_from_markdown(text: str) -> Optional[Any]:
    if not text or not isinstance(text, str):
        return None

    patterns = [
        r'```json\s*\n?(.*?)\n?\s*```',
        r'```\s*\n?(.*?)\n?\s*```',
        r'(\{[^`]*\})',
        r'(\[[^`]*\])',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            try:
                return json.loads(match.strip())
            except json.JSONDecodeError:
                continue

    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        logger.warning(f"Failed to extract JSON from text of length {len(text)}")
        return None

def extract_json_from_response(response: str) -> Optional[dict]:
    result = extract_json_from_markdown(response)
    if isinstance(result, dict):
        return result
    logger.warning(f"Expected dict, got {type(result).__name__}")
    return None

def extract_json_list_from_response(response: str) -> Optional[list]:
    result = extract_json_from_markdown(response)
    if isinstance(result, list):
        return result
    logger.warning(f"Expected list, got {type(result).__name__}")
    return None
