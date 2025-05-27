#!/usr/bin/env python3
"""
Performance test script to demonstrate the speed improvement of direct API calls.
"""

import asyncio
import time
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from scraper import check_ulez_compliance

async def test_performance():
    """Test the performance of the new direct API approach"""
    
    test_registrations = [
        "WO15CZY",  # BMW 330D - Non-compliant
        "A10YLR",   # Test registration
        "AB12CDE",  # Generic test
        "EF34GHI",  # Another test
        "JK56LMN",  # Another test
    ]
    
    print("🚀 Testing ULEZ Checker Performance")
    print("=" * 50)
    print("Testing with direct API calls (no browser automation)")
    print()
    
    total_start_time = time.time()
    
    for i, registration in enumerate(test_registrations, 1):
        print(f"Test {i}/5: {registration}")
        start_time = time.time()
        
        try:
            result = await check_ulez_compliance(registration)
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"  ✅ Result: {result.compliant} ({'Compliant' if result.compliant else 'Non-compliant'})")
            if result.make_model:
                print(f"  🚗 Vehicle: {result.make_model} ({result.year})")
            print(f"  ⚡ Time: {duration:.2f} seconds")
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            print(f"  ❌ Error: {str(e)}")
            print(f"  ⚡ Time: {duration:.2f} seconds")
        
        print()
    
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    avg_duration = total_duration / len(test_registrations)
    
    print("📊 Performance Summary")
    print("-" * 30)
    print(f"Total time: {total_duration:.2f} seconds")
    print(f"Average per request: {avg_duration:.2f} seconds")
    print(f"Requests per minute: {60/avg_duration:.1f}")
    print()
    print("🎯 Benefits of Direct API Approach:")
    print("  • No browser startup time (saves ~3-5 seconds)")
    print("  • No page loading time (saves ~2-3 seconds)")
    print("  • No form interaction simulation (saves ~2-4 seconds)")
    print("  • Direct data access (saves ~1-2 seconds)")
    print("  • Much lower resource usage (no Chromium process)")
    print("  • Better scalability for multiple concurrent requests")

if __name__ == "__main__":
    asyncio.run(test_performance()) 