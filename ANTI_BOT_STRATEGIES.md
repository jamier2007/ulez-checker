# Anti-Bot Evasion Strategies

This document outlines the comprehensive anti-bot detection evasion strategies implemented in the ULEZ checker application.

## 🛡️ Current Implementation

### 1. **Browser Fingerprint Evasion**
- **User Agent Rotation**: Rotates between realistic, recent browser user agents
- **Viewport Randomization**: Uses common screen resolutions (1920x1080, 1366x768, etc.)
- **WebDriver Detection Bypass**: Overrides `navigator.webdriver` property
- **Plugin Simulation**: Mocks browser plugins and languages
- **Chrome Object Injection**: Adds realistic Chrome runtime objects

### 2. **Human Behavior Simulation**
- **Realistic Typing**: Character-by-character input with random delays (50-150ms)
- **Mouse Movement**: Random mouse movements and realistic click patterns
- **Scroll Behavior**: Natural scrolling patterns before interaction
- **Session Establishment**: Visits main site before target page
- **Random Delays**: Variable delays between actions (1-5 seconds)

### 3. **Network-Level Evasion**
- **Header Rotation**: Realistic HTTP headers with proper Sec-Fetch values
- **Connection Pooling**: Proper TCP connection management
- **DNS Caching**: Realistic DNS behavior
- **Request Timing**: Random delays between API endpoint attempts
- **Session Persistence**: Maintains cookies and session state

### 4. **Stealth Browser Configuration**
```javascript
// Browser launch arguments for maximum stealth
--no-sandbox
--disable-setuid-sandbox
--disable-dev-shm-usage
--disable-accelerated-2d-canvas
--no-first-run
--no-zygote
--disable-gpu
--disable-background-timer-throttling
--disable-backgrounding-occluded-windows
--disable-renderer-backgrounding
--disable-features=TranslateUI
--disable-ipc-flooding-protection
--disable-web-security
--disable-features=VizDisplayCompositor
```

## 🚀 Advanced Strategies (Available)

### 1. **Proxy Rotation**
```python
# Configure in app/config.py
PROXY_LIST = [
    "http://user:pass@proxy1.example.com:8080",
    "http://user:pass@proxy2.example.com:8080",
]
```

### 2. **Residential Proxy Services**
- **Bright Data** (formerly Luminati)
- **Oxylabs**
- **Smartproxy**
- **ProxyMesh**

### 3. **CAPTCHA Solving Services**
- **2captcha**
- **Anti-Captcha**
- **CapMonster**
- **DeathByCaptcha**

### 4. **Browser Farm Rotation**
- Multiple browser instances
- Different browser types (Chrome, Firefox, Safari)
- Distributed across different IP ranges

## 🔧 Configuration Options

### Environment Variables
```bash
# Basic settings
HEADLESS=true
STEALTH_MODE=true
USE_PROXY=false

# Timing controls
MIN_REQUEST_DELAY=1.0
MAX_REQUEST_DELAY=5.0
RETRY_DELAY=2.0
MAX_RETRIES=3

# Feature toggles
ROTATE_USER_AGENTS=true
RANDOMIZE_VIEWPORT=true

# Proxy settings
PROXY_LIST="proxy1.com:8080,proxy2.com:8080"

# TfL API (if available)
TFL_API_KEY=your_api_key
TFL_APP_ID=your_app_id
```

## 📊 Detection Bypass Techniques

### 1. **Behavioral Analysis Evasion**
- **Variable Timing**: No fixed patterns in request timing
- **Human-like Errors**: Occasional typos and corrections
- **Realistic Navigation**: Following expected user journey
- **Session Duration**: Appropriate time spent on pages

### 2. **Technical Fingerprint Masking**
- **Canvas Fingerprinting**: Randomized canvas rendering
- **WebGL Fingerprinting**: Consistent but varied WebGL signatures
- **Audio Fingerprinting**: Realistic audio context properties
- **Font Detection**: Standard font lists for target OS

### 3. **Network Pattern Obfuscation**
- **Request Ordering**: Natural sequence of resource loading
- **Cache Behavior**: Realistic cache hit/miss patterns
- **Connection Reuse**: Proper HTTP/2 connection management
- **TLS Fingerprinting**: Standard TLS handshake patterns

## 🎯 Specific Anti-Detection Measures

### For Cloudflare Protection
```python
# Additional headers for Cloudflare bypass
headers.update({
    "CF-Connecting-IP": "1.2.3.4",  # Spoofed IP
    "CF-IPCountry": "GB",           # UK country code
    "CF-RAY": generate_cf_ray(),    # Fake CF-RAY header
})
```

### For Bot Detection Services
```python
# Disable automation indicators
await page.add_init_script("""
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
""")
```

### For Machine Learning Detection
- **Consistent Behavior**: Maintain behavioral consistency across sessions
- **Error Patterns**: Include realistic human error patterns
- **Timing Variance**: Natural variance in reaction times
- **Mouse Patterns**: Realistic mouse movement trajectories

## 🔄 Fallback Strategies

### 1. **API Endpoint Discovery**
- Reverse engineer actual API endpoints
- Monitor network traffic for API calls
- Use browser dev tools to find internal APIs

### 2. **Alternative Data Sources**
- TfL official API (if available)
- Government open data sources
- Third-party compliance checkers
- Cached/scraped data repositories

### 3. **Heuristic Estimation**
- Registration pattern analysis
- Year-based compliance estimation
- Make/model database lookup
- Euro standard inference

## 🚨 Legal and Ethical Considerations

### Best Practices
1. **Respect robots.txt**: Check and follow robots.txt guidelines
2. **Rate Limiting**: Don't overwhelm servers with requests
3. **Terms of Service**: Ensure compliance with website ToS
4. **Data Usage**: Only collect necessary data for legitimate purposes
5. **Attribution**: Provide proper attribution when required

### Risk Mitigation
- **IP Rotation**: Prevent IP-based blocking
- **Request Throttling**: Avoid triggering rate limits
- **Error Handling**: Graceful failure without retries on permanent blocks
- **Monitoring**: Track success rates and adjust strategies

## 📈 Success Metrics

### Key Performance Indicators
- **Success Rate**: Percentage of successful data extractions
- **Detection Rate**: Frequency of bot detection triggers
- **Response Time**: Average time to complete requests
- **Reliability**: Consistency across different times/conditions

### Monitoring and Alerting
```python
# Example monitoring
if success_rate < 0.8:
    logger.warning("High failure rate detected")
    switch_to_fallback_strategy()

if detection_events > threshold:
    logger.error("Bot detection triggered")
    rotate_proxy_and_user_agent()
```

## 🔮 Future Enhancements

### Planned Improvements
1. **Machine Learning Evasion**: AI-powered behavior simulation
2. **Browser Automation Detection**: Advanced WebDriver hiding
3. **Distributed Scraping**: Multi-node scraping architecture
4. **Real-time Adaptation**: Dynamic strategy adjustment
5. **Captcha Integration**: Automated captcha solving

### Research Areas
- **Behavioral Biometrics**: Human-like interaction patterns
- **Browser Exploitation**: Zero-day browser fingerprinting bypasses
- **Network Obfuscation**: Advanced traffic pattern masking
- **AI Detection Evasion**: Adversarial examples for bot detection ML models

---

**Note**: These techniques should only be used for legitimate purposes and in compliance with applicable laws and terms of service. Always respect website policies and rate limits. 