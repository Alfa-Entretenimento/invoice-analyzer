"""
AWS Lambda handler for Flask application
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
import serverless_wsgi

def handler(event, context):
    """
    AWS Lambda handler function
    """
    return serverless_wsgi.handle_request(app, event, context)