# Predefined chaos test scenarios

CHAOS_SCENARIOS = {
    "api_provider_down": {
        "name": "API Provider Down",
        "description": "Simulates primary AI model provider (e.g. Gemini) returning a 500 server error.",
        "severity": "high"
    },
    "api_rate_limited": {
        "name": "API Rate Limited",
        "description": "Simulates AI models returning 429 rate limit errors to trigger backoff controls.",
        "severity": "medium"
    },
    "api_timeout": {
        "name": "API Timeout",
        "description": "Simulates AI model inference latency of 10+ seconds to test timeout fallbacks.",
        "severity": "medium"
    },
    "redis_outage": {
        "name": "Redis Outage",
        "description": "Simulates broker disconnection, preventing Celery from fetching/scheduling tasks.",
        "severity": "critical"
    },
    "ats_form_change": {
        "name": "ATS Form Change",
        "description": "Simulates ATS payload validation rejections due to structural changes on application pages.",
        "severity": "high"
    },
    "all_ai_down": {
        "name": "All AI Providers Outage",
        "description": "Simulates complete loss of AI API connections. Triggers rule-based cache lookups.",
        "severity": "critical"
    }
}
