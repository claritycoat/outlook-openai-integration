# How the Updated System Works

## Overview

The system now creates draft responses for **ALL emails up to 4 days old** that haven't been replied to. This is perfect for people who struggle with inbox management and don't always move emails after replying.

## Email Processing Logic

### 1. Email Discovery
- **Scans emails** from the last 7 days
- **Filters to emails** up to 4 days old
- **Checks if you've already replied** to each email
- **Checks if a draft already exists** for each email

### 2. Draft Creation Rules

| Email Age | Action | Response Style |
|-----------|--------|----------------|
| **0 days** (new today) | Create draft immediately | Prompt, professional response |
| **1-4 days** | Create draft if no reply | Acknowledges delay, apologizes |
| **4+ days** | Ignore (too old) | No action |

### 3. Duplicate Prevention

The system prevents creating multiple drafts for the same email by:
- **Checking your Drafts folder** for existing responses
- **Looking for reply patterns** in your sent emails
- **Only creating one draft per email**

## Response Types

### For New Emails (0 days old)
```
Subject: Re: [Original Subject]
Content: Prompt, professional response that:
- Acknowledges the email immediately
- Addresses questions/concerns
- Maintains professional tone
- Includes proper greeting/closing
```

### For Older Emails (1-4 days old)
```
Subject: Re: [Original Subject]
Content: Response that:
- Acknowledges the delay (e.g., "Thank you for your email from 3 days ago")
- Apologizes for the late response
- Addresses the original content
- Maintains professional tone
- Includes proper greeting/closing
```

## Example Scenarios

### Scenario 1: New Email (Same Day)
- **Email received**: "Can you help with my project?"
- **System action**: Creates immediate draft
- **Draft response**: "Thank you for reaching out! I'd be happy to help with your project. Could you share more details about what you need?"

### Scenario 2: 2-Day-Old Email
- **Email received**: "Following up on our meeting"
- **System action**: Creates draft with delay acknowledgment
- **Draft response**: "Thank you for your email from 2 days ago. I apologize for the delay in responding. Regarding our meeting..."

### Scenario 3: Already Replied
- **Email received**: "Meeting request"
- **Your action**: You already replied
- **System action**: No draft created (detects your reply)

### Scenario 4: Draft Already Exists
- **Email received**: "Project update needed"
- **System action**: Previously created draft
- **Result**: No new draft (prevents duplicates)

## Benefits for Inbox Management

### 1. Immediate Drafts for New Emails
- **No more forgetting** to respond to new emails
- **Professional responses** ready to review and send
- **Consistent tone** across all communications

### 2. Catch-Up for Older Emails
- **Never miss** emails that slipped through
- **Professional delay acknowledgment** for older emails
- **Maintains relationships** even with delayed responses

### 3. Inbox Organization
- **Drafts folder** becomes your response queue
- **Easy to review** and modify responses
- **No more lost emails** in the inbox

## How to Use the System

### 1. Review Drafts Regularly
- **Check your Drafts folder** every day
- **Review and modify** responses as needed
- **Send responses** when ready

### 2. Train the AI
- **Add your best responses** to the training system
- **Create templates** for common scenarios
- **Improve response quality** over time

### 3. Monitor Performance
- **Check Vercel logs** for processing status
- **Review training statistics** to improve responses
- **Adjust settings** as needed

## Configuration Options

### Environment Variables
```env
DAYS_THRESHOLD=4          # Maximum age of emails to process
ALLOWED_DOMAINS=example.com # Optional domain filtering
```

### Cron Schedule
```json
{
  "crons": [
    {
      "path": "/api/outlook_openai",
      "schedule": "0 */6 * * *"  # Every 6 hours
    }
  ]
}
```

## Troubleshooting

### Common Issues

1. **No drafts being created**
   - Check if emails are actually up to 4 days old
   - Verify you haven't already replied
   - Check Vercel logs for errors

2. **Duplicate drafts**
   - System should prevent this automatically
   - Check Drafts folder for existing responses

3. **Wrong response tone**
   - Use training system to improve responses
   - Add more examples with your preferred tone

## Perfect for Inbox Management

This system is ideal for people who:
- **Struggle with inbox organization**
- **Forget to reply to emails**
- **Don't always move emails after replying**
- **Want professional responses ready to go**
- **Need help maintaining email relationships**

The system handles the heavy lifting while you focus on reviewing and sending the responses! 🚀 