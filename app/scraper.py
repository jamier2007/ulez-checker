import aiohttp
import json
import random
import asyncio
from typing import Optional
import logging

from app.models import UlezResponse

logger = logging.getLogger(__name__)

# User agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0",
]


async def fetch_ulez_data_direct_api(registration: str) -> Optional[UlezResponse]:
    """
    Use the discovered Motorway API endpoint directly for fast ULEZ checking.
    This bypasses browser automation entirely.
    """
    try:
        # Clean registration input
        registration = registration.strip().upper().replace(" ", "")
        
        # The actual API endpoint we discovered
        api_url = "https://api.motorway.co.uk/platform/v3/ulez/check"
        
        # Rotate user agents and add realistic headers
        user_agent = random.choice(USER_AGENTS)
        headers = {
            "User-Agent": user_agent,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://motorway.co.uk/ulez-checker",
            "Origin": "https://motorway.co.uk",
            "DNT": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Content-Type": "application/json",
        }
        
        # The payload format we observed from the browser
        payload = {
            "vrm": registration
        }
        
        connector = aiohttp.TCPConnector(
            limit=10,
            limit_per_host=5,
            ttl_dns_cache=300,
            use_dns_cache=True,
        )
        
        timeout = aiohttp.ClientTimeout(total=10, connect=3)
        
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=headers
        ) as session:
            logger.info(f"Making direct API call for registration: {registration}")
            
            async with session.post(api_url, json=payload) as response:
                logger.info(f"API response status: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"API response data: {data}")
                    
                    # Parse the response using the format we discovered
                    if data.get('status') == 'success' and 'data' in data:
                        api_data = data['data']
                        
                        # Extract vehicle information
                        make_display = api_data.get('make', {}).get('displayName', '') if isinstance(api_data.get('make'), dict) else str(api_data.get('make', ''))
                        model = api_data.get('model', '')
                        make_model = f"{make_display} {model}".strip() or None
                        
                        result = UlezResponse(
                            registration=registration,
                            compliant=api_data.get('isCompliant', False),
                            make_model=make_model,
                            year=api_data.get('year'),
                            engine_category=api_data.get('euroStatus'),
                            co2_emissions=api_data.get('emissions'),
                            charge=None if api_data.get('isCompliant') else 12.50,
                            message=f"Vehicle is {'compliant' if api_data.get('isCompliant') else 'not compliant'} with ULEZ standards"
                        )
                        
                        logger.info(f"Successfully parsed API response for {registration}")
                        return result
                    else:
                        logger.warning(f"API returned unexpected format: {data}")
                        
                elif response.status == 404:
                    logger.warning(f"Vehicle not found: {registration}")
                    return UlezResponse(
                        registration=registration,
                        compliant=False,
                        message="Vehicle not found in database. Please check the registration number."
                    )
                elif response.status == 429:
                    logger.warning(f"Rate limited for: {registration}")
                    return None  # Let it fall back to heuristics
                else:
                    logger.warning(f"API returned status {response.status}")
                    return None  # Let it fall back to heuristics
        
    except asyncio.TimeoutError:
        logger.error(f"API request timed out for {registration}")
    except Exception as e:
        logger.error(f"API request failed for {registration}: {str(e)}")
    
    return None


def estimate_compliance_heuristic(registration: str) -> UlezResponse:
    """
    Enhanced heuristic fallback based on UK registration patterns.
    UK format: AA## AAA (Area code + Age identifier + Random letters)
    """
    estimated_year = None
    estimated_compliant = False  # Default to non-compliant for safety
    
    try:
        # For modern UK plates (post-2001): AA## AAA format
        if len(registration) >= 4:
            # Age identifier is characters 2-4 (0-indexed: 2-3)
            age_code = registration[2:4]
            
            if age_code.isdigit():
                age_num = int(age_code)
                
                # UK age identifier system:
                # 01-50: March to August (first half of year)
                # 51-99: September to February (second half of year)
                if age_num <= 50:
                    estimated_year = 2001 + age_num
                else:
                    estimated_year = 2001 + (age_num - 50)
                
                logger.info(f"Parsed registration {registration}: age_code={age_code}, estimated_year={estimated_year}")
                
                # ULEZ compliance estimation
                if estimated_year >= 2015:  # Euro 6 diesel generally from 2015
                    estimated_compliant = True
                elif estimated_year >= 2006:  # Euro 4 petrol generally from 2006
                    estimated_compliant = True  # Assume petrol unless proven otherwise
                else:
                    estimated_compliant = False
            else:
                # Might be an older format or special plate
                logger.info(f"Non-numeric age code for {registration}: {age_code}")
                estimated_compliant = False
        else:
            # Too short to be a standard UK plate
            logger.info(f"Registration too short: {registration}")
            estimated_compliant = False
                
    except Exception as e:
        logger.warning(f"Error parsing registration {registration}: {str(e)}")
        estimated_compliant = False
    
    return UlezResponse(
        registration=registration.upper(),
        compliant=estimated_compliant,
        make_model=None,
        year=estimated_year,
        engine_category=None,
        co2_emissions=None,
        charge=12.50 if not estimated_compliant else None,
        message=f"Estimated result based on registration pattern. {'Likely compliant' if estimated_compliant else 'Likely non-compliant - may need to pay £12.50 daily charge'}. Please verify with official TfL checker."
    )


async def check_ulez_compliance(registration: str, show_browser: bool = False) -> UlezResponse:
    """
    Fast ULEZ compliance check using direct API calls.
    Browser automation is no longer needed!
    """
    try:
        # Clean registration input
        registration = registration.strip().upper().replace(" ", "")
        
        # Validate registration format
        if not registration or len(registration) < 2 or len(registration) > 8:
            raise ValueError("Invalid registration format")
        
        logger.info(f"Checking ULEZ compliance for registration: {registration}")
        
        # Try direct API call first (much faster!)
        logger.info("Attempting direct API call...")
        result = await fetch_ulez_data_direct_api(registration)
        if result:
            logger.info("Successfully got result from direct API call")
            return result
        
        # Enhanced heuristic fallback if API fails
        logger.warning("Direct API failed, using enhanced heuristics")
        return estimate_compliance_heuristic(registration)
        
    except ValueError as e:
        raise e
    except Exception as e:
        logger.error(f"Error checking compliance for {registration}: {str(e)}")
        raise Exception(f"Error checking ULEZ compliance: {str(e)}")
