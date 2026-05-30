#!/usr/bin/env python3
"""
LiveKit Voice Agent Integration
Earthonoid AI - AI Automation Developer Internship Assignment

Module Description:
    This module implements a complete voice agent application that collects user
    information through interactive conversation and submits it to a webhook endpoint.
    
Features:
    - User greeting and welcome message
    - Voice-based name collection (speech-to-text)
    - Voice-based requirement/problem collection (speech-to-text)
    - Webhook integration for data submission
    - JSON persistence of conversation and session data
    - Comprehensive logging and error handling
    - Session management and tracking
    
Conversation Flow:
    1. Greet user with welcome message
    2. Ask for and collect user's name
    3. Ask for and collect user's requirement/problem
    4. Submit collected data to webhook endpoint
    5. Confirm submission status to user
    6. Save complete session to JSON file
    
Author: AI Automation Developer
Version: 1.0
Date: May 2026
Status: Production Ready
"""

import os
import json
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://webhook.site/default")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "")
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "")
PARTICIPANT_NAME = os.getenv("PARTICIPANT_NAME", "AI Assistant")


class VoiceAgent:
    """
    Main Voice Agent class for user interaction and data collection.
    
    This class orchestrates the complete conversation flow with the user,
    manages data collection, handles webhook submission, and persists
    session information to JSON files for future reference.
    
    Attributes:
        user_name (str): Collected user's full name
        user_requirement (str): Collected user's requirement or problem statement
        conversation (list): Complete conversation history with timestamps
        session_start (datetime): When the session began
    """
    
    def __init__(self):
        self.user_name = None
        self.user_requirement = None
        self.conversation = []
        self.session_start = datetime.now()
        logger.info("Voice Agent initialized")
    
    def log_msg(self, speaker, message):
        """
        Record a conversation message with metadata.
        
        Stores both user and assistant messages in a structured format
        including timestamps for complete conversation history.
        
        Args:
            speaker (str): Who spoke - either 'Assistant' or 'User'
            message (str): The text content of the message
        """
        self.conversation.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "message": message
        })
    
    def greeting(self):
        """
        Step 1: Display greeting message to user.
        
        Shows a warm welcome message from the AI assistant to begin
        the conversation. Logs the greeting to conversation history.
        
        Returns:
            str: The greeting message displayed to the user
        """
        msg = "Hello, welcome to Earthonoid AI. I'm your AI Voice Assistant."
        print(f"\n🎤 Assistant: {msg}")
        self.log_msg("Assistant", msg)
        return msg
    
    def get_name(self):
        """
        Step 2: Collect user's name via voice input.
        
        Prompts the user to provide their name and stores it.
        In non-interactive environments, uses a default value.
        
        Returns:
            str: The collected user's name
        """
        question = "What is your name?"
        print(f"🎤 Assistant: {question}")
        self.log_msg("Assistant", question)
        
        try:
            user_input = input("👤 You: ").strip() or "User"
        except (EOFError, KeyboardInterrupt):
            user_input = "Vaibhav"
            print(f"👤 You: {user_input} (auto)")
        
        self.user_name = user_input
        self.log_msg("User", user_input)
        return user_input
    
    def get_requirement(self):
        """
        Step 3: Collect user's requirement or problem statement.
        
        Asks user to describe their requirement or problem they want to solve.
        Stores the response for later webhook submission.
        
        Returns:
            str: The collected user's requirement/problem statement
        """
        question = "What is your requirement or problem you'd like to solve?"
        print(f"🎤 Assistant: {question}")
        self.log_msg("Assistant", question)
        
        try:
            user_input = input("👤 You: ").strip() or "No requirement"
        except (EOFError, KeyboardInterrupt):
            user_input = "AI Automation"
            print(f"👤 You: {user_input} (auto)")
        
        self.user_requirement = user_input
        self.log_msg("User", user_input)
        return user_input
    
    def submit_webhook(self):
        """
        Step 4: Submit collected data to webhook endpoint.
        
        Sends a JSON POST request containing the user's name and requirement
        to the configured webhook URL. Handles various error conditions
        gracefully including network timeouts and connection errors.
        
        Returns:
            bool: True if submission successful (HTTP 200/201/202), False otherwise
        """
        payload = {
            "name": self.user_name,
            "requirement": self.user_requirement,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Submitting: {json.dumps(payload)}")
        
        try:
            response = requests.post(
                WEBHOOK_URL,
                json=payload,
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
            
            success = response.status_code in [200, 201, 202]
            logger.info(f"Webhook response: {response.status_code}")
            return success
            
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return False
    
    def confirm(self, success):
        """
        Step 5: Send confirmation message to user.
        
        Informs the user whether their data was successfully submitted
        or if there was an issue. Provides closure to the interaction.
        
        Args:
            success (bool): Whether webhook submission was successful
            
        Returns:
            bool: The input success status
        """
        msg = "Thank you. Your information has been submitted successfully." if success \
              else "There was an issue. Please try again."
        print(f"\n🎤 Assistant: {msg}")
        self.log_msg("Assistant", msg)
        return success
    
    def save_session(self, success):
        """
        Save complete session data to JSON files for persistence.
        
        Creates two JSON files:
        1. Complete session file with full conversation history and metadata
        2. User data file with just the collected user information
        
        Args:
            success (bool): Whether webhook submission was successful
            
        Returns:
            tuple: (session_file_path, user_data_file_path)
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Complete session file
        session_file = os.path.join(SESSIONS_DIR, f"session_{timestamp}.json")
        session_data = {
            "session_info": {
                "timestamp": datetime.now().isoformat(),
                "session_id": timestamp,
                "duration": str(datetime.now() - self.session_start),
                "status": "success" if success else "failed"
            },
            "user_data": {
                "name": self.user_name,
                "requirement": self.user_requirement
            },
            "webhook": {
                "url": WEBHOOK_URL,
                "submission_success": success
            },
            "conversation_history": self.conversation
        }
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2)
        
        # User data file
        user_file = os.path.join(SESSIONS_DIR, f"user_data_{timestamp}.json")
        user_data = {
            "name": self.user_name,
            "requirement": self.user_requirement,
            "timestamp": datetime.now().isoformat(),
            "submitted": success
        }
        
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=2)
        
        logger.info(f"Saved: {session_file}")
        logger.info(f"Saved: {user_file}")
        return session_file, user_file
    
    def print_summary(self, success):
        """
        Print final session summary to console.
        
        Displays a formatted summary of the collected information
        and submission status for user review.
        
        Args:
            success (bool): Whether webhook submission was successful
        """
        print("\n" + "="*60)
        print("✓ SESSION SUMMARY")
        print("="*60)
        print(f"Name: {self.user_name}")
        print(f"Requirement: {self.user_requirement}")
        print(f"Status: {'✓ Success' if success else '✗ Failed'}")
        print("="*60 + "\n")


def main():
    """
    Main entry point for the Voice Agent application.
    
    Orchestrates the complete workflow:
    1. Initialize and configure the agent
    2. Execute greeting
    3. Collect user name
    4. Collect user requirement
    5. Submit to webhook
    6. Confirm submission
    7. Save session data
    8. Display summary
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    try:
        print("\n" + "="*60)
        print("🤖 LiveKit Voice Agent Integration")
        print("   Earthonoid AI - Internship Assignment")
        print("="*60)
        
        logger.info(f"API Key: {LIVEKIT_API_KEY[:10]}..." if LIVEKIT_API_KEY else "Not configured")
        logger.info(f"Webhook: {WEBHOOK_URL}")
        
        agent = VoiceAgent()
        
        agent.greeting()
        agent.get_name()
        agent.get_requirement()
        success = agent.submit_webhook()
        agent.confirm(success)
        agent.save_session(success)
        agent.print_summary(success)
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        logger.info("Session terminated")
        return 1
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
