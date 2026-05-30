#!/usr/bin/env python3
"""
Voice Agent Integration - Automated Test Suite
Earthonoid AI - Testing Module

Module Description:
    This module provides automated testing for the Voice Agent Integration.
    It simulates the complete conversation flow without requiring user input,
    and validates webhook submission functionality.
    
Features:
    - Automated conversation simulation
    - Webhook submission testing  
    - Session data persistence to JSON
    - Configuration validation
    - Error handling and logging
    
Usage:
    python voice_agent_test.py
    
Version: 1.0
"""

import os
import json
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")

def validate_config():
    """Validate environment"""
    required = ["WEBHOOK_URL", "LIVEKIT_API_KEY"]
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        raise ValueError(f"Missing: {', '.join(missing)}")
    logger.info(f"✓ API Key: {LIVEKIT_API_KEY[:10]}...")
    logger.info(f"✓ Webhook: {WEBHOOK_URL}")

def send_webhook(name, requirement):
    """Send to webhook"""
    payload = {"name": name, "requirement": requirement}
    logger.info(f"Sending: {json.dumps(payload)}")
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        success = response.status_code in [200, 201, 202]
        logger.info(f"Status: {response.status_code}")
        return success
    except Exception as e:
        logger.error(f"Error: {e}")
        return False

def save_session(name, requirement, success):
    """Save to JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_file = os.path.join(SESSIONS_DIR, f"session_{timestamp}.json")
    data = {
        "timestamp": datetime.now().isoformat(),
        "session_id": timestamp,
        "user_data": {"name": name, "requirement": requirement},
        "webhook_success": success
    }
    with open(session_file, 'w') as f:
        json.dump(data, f, indent=2)
    logger.info(f"Saved: {session_file}")
    return session_file

def main():
    """Main test"""
    try:
        print("\n" + "="*60)
        print("🤖 Voice Agent - Automated Test")
        print("="*60)
        
        validate_config()
        
        print("\n📊 CONVERSATION:")
        print("-"*60)
        print("🎤 Assistant: Hello, welcome to Earthonoid AI.")
        
        name = "Vaibhav"
        print(f"👤 User: {name}")
        
        requirement = "AI Automation"
        print(f"👤 User: {requirement}")
        
        success = send_webhook(name, requirement)
        
        msg = "Thank you. Your information has been submitted successfully." if success \
              else "There was an issue. Please try again."
        print(f"\n🎤 Assistant: {msg}")
        
        session_file = save_session(name, requirement, success)
        
        print("\n" + "="*60)
        print("✓ TEST SUMMARY")
        print("="*60)
        print(f"Name: {name}")
        print(f"Requirement: {requirement}")
        print(f"Status: {'✓ Success' if success else '✗ Failed'}")
        print(f"Saved: {session_file}")
        print("="*60 + "\n")
        
        return 0 if success else 1
        
    except ValueError as e:
        logger.error(f"Config Error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
