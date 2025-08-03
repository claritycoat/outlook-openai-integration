#!/usr/bin/env python3
"""
Training System for Outlook-OpenAI Integration
Allows you to teach the AI how to construct better replies
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TrainingExample:
    """Represents a training example for email responses."""
    original_email: str
    your_response: str
    email_type: str  # e.g., "inquiry", "complaint", "follow-up", "general"
    tone: str  # e.g., "professional", "friendly", "formal", "casual"
    key_points: List[str]  # What you want the AI to focus on
    created_date: datetime = None
    
    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now()

@dataclass
class ResponseTemplate:
    """Represents a response template for different email types."""
    name: str
    email_type: str
    tone: str
    template: str
    variables: List[str]  # Placeholders like {sender_name}, {delay_apology}
    created_date: datetime = None
    
    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now()

class TrainingSystem:
    """Manages training data and customizes AI responses."""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.training_file = 'training_data.json'
        self.templates_file = 'response_templates.json'
        self.load_training_data()
        self.load_templates()
    
    def load_training_data(self):
        """Load existing training examples."""
        try:
            if os.path.exists(self.training_file):
                with open(self.training_file, 'r') as f:
                    data = json.load(f)
                    self.training_examples = [
                        TrainingExample(**example) for example in data
                    ]
            else:
                self.training_examples = []
        except Exception as e:
            logger.error(f"Error loading training data: {e}")
            self.training_examples = []
    
    def save_training_data(self):
        """Save training examples to file."""
        try:
            data = [asdict(example) for example in self.training_examples]
            with open(self.training_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            logger.info(f"Saved {len(self.training_examples)} training examples")
        except Exception as e:
            logger.error(f"Error saving training data: {e}")
    
    def load_templates(self):
        """Load response templates."""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'r') as f:
                    data = json.load(f)
                    self.templates = [
                        ResponseTemplate(**template) for template in data
                    ]
            else:
                self.templates = []
        except Exception as e:
            logger.error(f"Error loading templates: {e}")
            self.templates = []
    
    def save_templates(self):
        """Save response templates to file."""
        try:
            data = [asdict(template) for template in self.templates]
            with open(self.templates_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            logger.info(f"Saved {len(self.templates)} response templates")
        except Exception as e:
            logger.error(f"Error saving templates: {e}")
    
    def add_training_example(self, original_email: str, your_response: str, 
                           email_type: str, tone: str, key_points: List[str]):
        """Add a new training example."""
        example = TrainingExample(
            original_email=original_email,
            your_response=your_response,
            email_type=email_type,
            tone=tone,
            key_points=key_points
        )
        self.training_examples.append(example)
        self.save_training_data()
        logger.info(f"Added training example for {email_type} email with {tone} tone")
    
    def add_response_template(self, name: str, email_type: str, tone: str, 
                           template: str, variables: List[str]):
        """Add a new response template."""
        template_obj = ResponseTemplate(
            name=name,
            email_type=email_type,
            tone=tone,
            template=template,
            variables=variables
        )
        self.templates.append(template_obj)
        self.save_templates()
        logger.info(f"Added response template: {name}")
    
    def get_training_context(self, email_type: str = None, tone: str = None) -> str:
        """Generate training context for AI based on examples."""
        if not self.training_examples:
            return ""
        
        # Filter examples by type and tone if specified
        filtered_examples = self.training_examples
        if email_type:
            filtered_examples = [e for e in filtered_examples if e.email_type == email_type]
        if tone:
            filtered_examples = [e for e in filtered_examples if e.tone == tone]
        
        if not filtered_examples:
            return ""
        
        context = "Based on these training examples, generate similar responses:\n\n"
        
        for i, example in enumerate(filtered_examples[:5], 1):  # Limit to 5 examples
            context += f"Example {i}:\n"
            context += f"Original Email: {example.original_email}\n"
            context += f"Your Response: {example.your_response}\n"
            context += f"Type: {example.email_type}, Tone: {example.tone}\n"
            context += f"Key Points: {', '.join(example.key_points)}\n\n"
        
        return context
    
    def get_template_context(self, email_type: str = None) -> str:
        """Generate template context for AI."""
        if not self.templates:
            return ""
        
        filtered_templates = self.templates
        if email_type:
            filtered_templates = [t for t in self.templates if t.email_type == email_type]
        
        if not filtered_templates:
            return ""
        
        context = "Use these response templates as guidance:\n\n"
        
        for template in filtered_templates[:3]:  # Limit to 3 templates
            context += f"Template: {template.name}\n"
            context += f"Type: {template.email_type}, Tone: {template.tone}\n"
            context += f"Template: {template.template}\n"
            context += f"Variables: {', '.join(template.variables)}\n\n"
        
        return context
    
    def generate_customized_response(self, email_content: str, email_type: str = None, 
                                   tone: str = None, days_old: int = 0) -> str:
        """Generate a response using training data and templates."""
        try:
            # Build the prompt with training context
            training_context = self.get_training_context(email_type, tone)
            template_context = self.get_template_context(email_type)
            
            prompt = f"""
You are a professional email assistant. Generate a response to the following email.

{training_context}
{template_context}

Original Email:
{email_content}

Email Age: {days_old} days old
Email Type: {email_type or 'general'}
Desired Tone: {tone or 'professional'}

Please generate a response that:
1. Acknowledges the delay if the email is old
2. Addresses the content appropriately
3. Matches the tone and style of the training examples
4. Uses templates as guidance when applicable
5. Is professional and courteous

Response:
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional email assistant that learns from training examples and templates."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating customized response: {e}")
            return None
    
    def analyze_email_type(self, email_content: str) -> str:
        """Analyze email content to determine its type."""
        try:
            prompt = f"""
Analyze this email and classify it into one of these types:
- inquiry (asking for information)
- complaint (expressing dissatisfaction)
- follow-up (checking on previous communication)
- request (asking for action)
- general (general communication)

Email content:
{email_content}

Respond with just the type (e.g., "inquiry"):
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip().lower()
            
        except Exception as e:
            logger.error(f"Error analyzing email type: {e}")
            return "general"
    
    def get_training_stats(self) -> Dict:
        """Get statistics about training data."""
        stats = {
            "total_examples": len(self.training_examples),
            "total_templates": len(self.templates),
            "email_types": {},
            "tones": {}
        }
        
        for example in self.training_examples:
            stats["email_types"][example.email_type] = stats["email_types"].get(example.email_type, 0) + 1
            stats["tones"][example.tone] = stats["tones"].get(example.tone, 0) + 1
        
        return stats

def interactive_training():
    """Interactive training session."""
    training_system = TrainingSystem()
    
    print("🎓 Outlook-OpenAI Training System")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Add training example")
        print("2. Add response template")
        print("3. View training stats")
        print("4. Test customized response")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            print("\n📝 Adding Training Example")
            print("-" * 30)
            
            original_email = input("Original email content: ")
            your_response = input("Your response: ")
            email_type = input("Email type (inquiry/complaint/follow-up/request/general): ")
            tone = input("Tone (professional/friendly/formal/casual): ")
            key_points = input("Key points (comma-separated): ").split(",")
            
            training_system.add_training_example(
                original_email.strip(),
                your_response.strip(),
                email_type.strip(),
                tone.strip(),
                [point.strip() for point in key_points]
            )
            
        elif choice == "2":
            print("\n📋 Adding Response Template")
            print("-" * 30)
            
            name = input("Template name: ")
            email_type = input("Email type: ")
            tone = input("Tone: ")
            template = input("Template (use {variables}): ")
            variables = input("Variables (comma-separated): ").split(",")
            
            training_system.add_response_template(
                name.strip(),
                email_type.strip(),
                tone.strip(),
                template.strip(),
                [var.strip() for var in variables]
            )
            
        elif choice == "3":
            print("\n📊 Training Statistics")
            print("-" * 30)
            
            stats = training_system.get_training_stats()
            print(f"Total examples: {stats['total_examples']}")
            print(f"Total templates: {stats['total_templates']}")
            print(f"Email types: {stats['email_types']}")
            print(f"Tones: {stats['tones']}")
            
        elif choice == "4":
            print("\n🧪 Test Customized Response")
            print("-" * 30)
            
            email_content = input("Email content to respond to: ")
            email_type = input("Email type (or press Enter to auto-detect): ")
            tone = input("Desired tone (or press Enter for professional): ")
            days_old = input("Days old (or press Enter for 0): ")
            
            if not email_type:
                email_type = training_system.analyze_email_type(email_content)
                print(f"Auto-detected email type: {email_type}")
            
            if not tone:
                tone = "professional"
            
            if not days_old:
                days_old = 0
            
            response = training_system.generate_customized_response(
                email_content,
                email_type,
                tone,
                int(days_old)
            )
            
            if response:
                print(f"\nGenerated Response:\n{response}")
            else:
                print("Failed to generate response")
                
        elif choice == "5":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid option. Please select 1-5.")

if __name__ == "__main__":
    interactive_training() 