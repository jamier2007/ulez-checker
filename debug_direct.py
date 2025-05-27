#!/usr/bin/env python3
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from scraper import check_ulez_compliance

async def test():
    result = await check_ulez_compliance('WO15CZY')
    print(f'Type: {type(result)}')
    print(f'Compliant: {result.compliant}')
    print(f'Year: {result.year}')
    print(f'Dict: {result.dict()}')

if __name__ == "__main__":
    asyncio.run(test()) 