#!/usr/bin/env python3
"""
Test script to run the ULEZ scraper with visible browser for debugging.
"""

import asyncio
import logging
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from scraper import check_ulez_compliance

# Set up logging to see what's happening
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('debug.log')
    ]
)

async def test_scraper():
    """Test the scraper with visible browser"""
    registration = "WO15CZY"
    
    print(f"\n🚗 Testing ULEZ compliance check for: {registration}")
    print("=" * 50)
    print("This will open a browser window so you can see what's happening.")
    print("The browser will stay open for 1 minute after completion for inspection.")
    print("Press Ctrl+C to close early if needed.")
    print("=" * 50)
    
    try:
        result = await check_ulez_compliance(registration, show_browser=True)
        
        print(f"\n✅ Result for {registration}:")
        print("-" * 30)
        print(f"registration: {result.registration}")
        print(f"compliant: {result.compliant}")
        print(f"make_model: {result.make_model}")
        print(f"year: {result.year}")
        print(f"engine_category: {result.engine_category}")
        print(f"co2_emissions: {result.co2_emissions}")
        print(f"charge: {result.charge}")
        print(f"message: {result.message}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        
    print(f"\n📁 Debug files created:")
    print("- debug.log (detailed logs)")
    print("- debug_page_loaded.png (screenshot after page load)")
    print("- debug_after_typing.png (screenshot after typing registration)")
    print("- debug_after_submit.png (screenshot after clicking submit)")
    print("- debug_page_content.html (final page HTML content)")

if __name__ == "__main__":
    asyncio.run(test_scraper()) 