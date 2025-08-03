#!/usr/bin/env python3
"""
Health check endpoint for Vercel
"""

import os
import json

def handler(request, context):
    """Simple health check handler."""
    try:
        # Check environment variables
        env_vars = {
            'CLIENT_ID': bool(os.getenv('CLIENT_ID')),
            'CLIENT_SECRET': bool(os.getenv('CLIENT_SECRET')),
            'TENANT_ID': bool(os.getenv('TENANT_ID')),
            'OPENAI_API_KEY': bool(os.getenv('OPENAI_API_KEY')),
            'DAYS_THRESHOLD': bool(os.getenv('DAYS_THRESHOLD')),
            'ALLOWED_DOMAINS': bool(os.getenv('ALLOWED_DOMAINS'))
        }
        
        # Check which variables are missing
        missing_vars = [key for key, value in env_vars.items() if not value]
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': 'healthy',
                'environment_variables': {
                    'present': [key for key, value in env_vars.items() if value],
                    'missing': missing_vars
                },
                'total_vars': len(env_vars),
                'present_count': len([v for v in env_vars.values() if v])
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