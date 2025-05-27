import os
from typing import List, Optional

class AntiDetectionConfig:
    """Configuration for anti-bot detection measures"""
    
    # Proxy settings (add your proxy list here)
    PROXY_LIST: List[str] = [
        # Example format: "http://username:password@proxy-server:port"
        # "http://user:pass@proxy1.example.com:8080",
        # "http://user:pass@proxy2.example.com:8080",
    ]
    
    # Rate limiting
    MIN_REQUEST_DELAY = float(os.getenv("MIN_REQUEST_DELAY", "1.0"))
    MAX_REQUEST_DELAY = float(os.getenv("MAX_REQUEST_DELAY", "5.0"))
    
    # Browser settings
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    STEALTH_MODE = os.getenv("STEALTH_MODE", "true").lower() == "true"
    
    # Retry settings
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY = float(os.getenv("RETRY_DELAY", "2.0"))
    
    # User agent rotation
    ROTATE_USER_AGENTS = os.getenv("ROTATE_USER_AGENTS", "true").lower() == "true"
    
    # Viewport randomization
    RANDOMIZE_VIEWPORT = os.getenv("RANDOMIZE_VIEWPORT", "true").lower() == "true"
    
    # Alternative data sources (fallback APIs)
    FALLBACK_APIS: List[str] = [
        # Add alternative ULEZ checking APIs here
        # "https://api.tfl.gov.uk/Vehicle/UlezCompliance",  # Example
    ]
    
    # TfL API settings (if available)
    TFL_API_KEY = os.getenv("TFL_API_KEY")
    TFL_APP_ID = os.getenv("TFL_APP_ID")
    
    @classmethod
    def get_proxy(cls) -> Optional[str]:
        """Get a random proxy from the list"""
        if not cls.PROXY_LIST:
            return None
        import random
        return random.choice(cls.PROXY_LIST)
    
    @classmethod
    def should_use_proxy(cls) -> bool:
        """Determine if we should use a proxy for this request"""
        return bool(cls.PROXY_LIST) and os.getenv("USE_PROXY", "false").lower() == "true" 