#!/usr/bin/env python3
"""
Simple test function to debug deployment issues
"""

import os
import json

def handler(request, context):
    """Simple test handler."""
    try:
        # Check environment variables
        env_vars = {
            "CLIENT_ID": os.getenv('CLIENT_ID', 'NOT_SET'),
            "CLIENT_SECRET": os.getenv('CLIENT_SECRET', 'NOT_SET'),
            "TENANT_ID": os.getenv('TENANT_ID', 'NOT_SET'),
            "OPENAI_API_KEY": os.getenv('OPENAI_API_KEY', 'NOT_SET'),
            "DAYS_THRESHOLD": os.getenv('DAYS_THRESHOLD', 'NOT_SET'),
        }
        
        # Check if any are missing
        missing_vars = [k for k, v in env_vars.items() if v == 'NOT_SET']
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': 'Test function working',
                'environment_variables': env_vars,
                'missing_variables': missing_vars,
                'python_version': os.sys.version
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': str(e),
                'type': type(e).__name__
            })
        } 