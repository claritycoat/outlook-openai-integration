# Training Guide: Teaching Your AI Email Assistant

Learn how to train your Outlook-OpenAI integration to generate better, more personalized email responses.

## Why Train Your AI?

The default AI responses are good, but they're generic. By training the system with your own examples, you can:

- **Match your writing style** and tone
- **Handle specific scenarios** better (complaints, inquiries, follow-ups)
- **Use your preferred language** and terminology
- **Include your company's policies** and procedures
- **Create more authentic responses** that sound like you

## Getting Started

### 1. Start the Training System

```bash
python training_system.py
```

### 2. Add Your First Training Example

When you see a good email response you've written, add it to the training system:

1. **Original Email**: Copy the email you received
2. **Your Response**: Copy your actual reply
3. **Email Type**: Classify it (inquiry, complaint, follow-up, request, general)
4. **Tone**: Describe the tone (professional, friendly, formal, casual)
5. **Key Points**: What you focused on in your response

### Example Training Session

```
📝 Adding Training Example
------------------------------
Original email content: Hi, I'm interested in your services. Can you send me a quote for a website redesign?

Your response: Thank you for your interest in our services! I'd be happy to provide you with a quote for your website redesign. To give you the most accurate estimate, could you please share some details about your current website and what specific changes you're looking for?

Email type: inquiry
Tone: professional
Key points: acknowledge interest, request more details, professional tone
```

## Training Strategies

### 1. Start with Common Scenarios

Begin with emails you receive frequently:

- **Inquiries about services/products**
- **Complaints or concerns**
- **Follow-up requests**
- **General questions**
- **Meeting requests**

### 2. Include Different Tones

Train the AI with various tones to handle different situations:

- **Professional**: For formal business communications
- **Friendly**: For existing clients or casual inquiries
- **Formal**: For official correspondence
- **Casual**: For internal team communications

### 3. Add Response Templates

Create templates for recurring situations:

```
📋 Adding Response Template
------------------------------
Template name: Service Inquiry Response
Email type: inquiry
Tone: professional
Template: Thank you for your interest in our {service_name}. I'd be happy to help you with {specific_request}. To provide you with the most accurate information, could you please share {required_details}?

Variables: service_name, specific_request, required_details
```

## Advanced Training Techniques

### 1. Email Type Classification

The system automatically classifies emails into these types:

- **inquiry**: Asking for information
- **complaint**: Expressing dissatisfaction
- **follow-up**: Checking on previous communication
- **request**: Asking for action
- **general**: General communication

### 2. Tone Matching

Train responses for different tones:

- **Professional**: "I appreciate your inquiry and would be happy to assist you..."
- **Friendly**: "Thanks for reaching out! I'd love to help you with..."
- **Formal**: "We acknowledge receipt of your communication regarding..."
- **Casual**: "Hey! Thanks for the message. Let me help you with..."

### 3. Key Points to Focus On

When adding training examples, include key points like:

- **Acknowledgment**: How you acknowledge the sender
- **Apology**: How you handle delays or issues
- **Information gathering**: How you ask for more details
- **Next steps**: How you outline what happens next
- **Closing**: How you end your emails

## Best Practices

### 1. Quality Over Quantity

- **10-15 good examples** are better than 50 mediocre ones
- **Focus on your best responses** that you'd want to replicate
- **Include variety** in tone, length, and complexity

### 2. Be Specific

- **Include context** about why you responded the way you did
- **Note special circumstances** (urgent requests, VIP clients, etc.)
- **Mention company policies** or procedures you followed

### 3. Regular Updates

- **Review and update** training data monthly
- **Add new scenarios** as they come up
- **Remove outdated examples** that no longer reflect your style

## Testing Your Training

### 1. Test with Real Emails

Use the "Test Customized Response" option to see how your training affects responses:

```
🧪 Test Customized Response
------------------------------
Email content to respond to: [paste a real email]
Email type: [or let it auto-detect]
Desired tone: professional
Days old: 3
```

### 2. Compare Results

Test the same email with and without training to see the difference:

- **Before training**: Generic, professional response
- **After training**: Personalized, matches your style

### 3. Iterate and Improve

- **If responses aren't quite right**, add more examples
- **If tone is off**, add more examples with that specific tone
- **If certain scenarios aren't handled well**, add more examples for that email type

## Training Examples by Scenario

### Customer Service Inquiries

**Original**: "I have a problem with my order #12345"
**Your Response**: "I'm sorry to hear you're having an issue with your order. Let me look into this right away. Could you please provide more details about what specific problem you're experiencing?"

**Key Points**: Acknowledge the problem, show empathy, ask for details

### Follow-up Requests

**Original**: "Just checking in on the proposal I sent last week"
**Your Response**: "Thanks for following up! I've been working on your proposal and should have it ready by Friday. I'll send it over as soon as it's complete."

**Key Points**: Acknowledge the follow-up, provide status update, set expectations

### Meeting Requests

**Original**: "Can we schedule a call to discuss the project?"
**Your Response**: "Absolutely! I'd love to discuss the project with you. I'm available Tuesday and Thursday afternoon. What works best for you?"

**Key Points**: Show enthusiasm, offer specific times, make it easy to respond

## Monitoring and Maintenance

### 1. Check Training Stats

Regularly review your training statistics:

```
📊 Training Statistics
------------------------------
Total examples: 15
Total templates: 3
Email types: {'inquiry': 8, 'complaint': 3, 'follow-up': 4}
Tones: {'professional': 10, 'friendly': 5}
```

### 2. Balance Your Training Data

Ensure you have good coverage across:
- **Email types**: Don't focus only on inquiries
- **Tones**: Include different tones for variety
- **Scenarios**: Cover different business situations

### 3. Update Based on Results

- **If certain emails aren't getting good responses**, add more examples
- **If responses are too generic**, add more specific examples
- **If tone is inconsistent**, add more examples with clear tone indicators

## Troubleshooting

### Common Issues

1. **Responses too generic**
   - Add more specific examples
   - Include more context in key points

2. **Wrong tone**
   - Add more examples with the desired tone
   - Be more explicit about tone classification

3. **Missing key information**
   - Add examples that include the missing elements
   - Update key points to emphasize important aspects

4. **Responses too long/short**
   - Add examples with your preferred length
   - Note length preferences in key points

## Integration with Vercel Deployment

When you deploy to Vercel, your training data will be included in the deployment:

1. **Training data files** (`training_data.json`, `response_templates.json`) are deployed with your code
2. **The AI will use your training** to generate better responses
3. **You can update training** by redeploying with new training data

## Next Steps

1. **Start with 5-10 good examples** from your email history
2. **Test the system** with real emails
3. **Add more examples** based on the results
4. **Deploy to Vercel** to use your trained AI
5. **Continue training** as you find better examples

Remember: The more you train, the better your AI will become at sounding like you! 🚀 