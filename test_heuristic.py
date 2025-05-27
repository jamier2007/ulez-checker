#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from scraper import estimate_compliance_heuristic

# Test the heuristic function
result = estimate_compliance_heuristic('WO15CZY')
print(f'Registration: {result.registration}')
print(f'Compliant: {result.compliant}')
print(f'Year: {result.year}')
print(f'Charge: {result.charge}')
print(f'Message: {result.message}') 