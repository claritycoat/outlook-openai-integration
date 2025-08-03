# Quick Start Guide

Get your Outlook-OpenAI integration running in 10 minutes!

## Step 1: Install Dependencies

```bash
python setup.py
```

This will install all required packages and create your `.env` file.

## Step 2: Get Your Credentials

### Microsoft Azure App Registration (5 minutes)

1. Go to [Azure Portal](https://portal.azure.com)
2. Search for "App registrations" → "New registration"
3. Name: "Outlook-OpenAI Integration"
4. Account type: "Accounts in this organizational directory only"
5. Click "Register"
6. Copy the **Application (client) ID** and **Directory (tenant) ID**

#### Add Permissions:
1. Go to "API permissions" → "Add a permission"
2. Select "Microsoft Graph" → "Application permissions"
3. Add: `Mail.Read`, `Mail.ReadWrite`, `Mail.Send`
4. Click "Grant admin consent"

#### Create Secret:
1. Go to "Certificates & secrets" → "New client secret"
2. Add description and choose expiration
3. **Copy the secret value immediately**

### OpenAI API Key (2 minutes)

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create new API key
3. Copy the key (starts with `sk-`)

## Step 3: Configure Environment

Edit the `.env` file with your credentials:

```env
CLIENT_ID=your_azure_client_id
CLIENT_SECRET=your_azure_client_secret
TENANT_ID=your_azure_tenant_id
OPENAI_API_KEY=your_openai_api_key
```

## Step 4: Test Your Setup

```bash
python test_setup.py
```

This will verify everything is working correctly.

## Step 5: Run the Integration

```bash
python outlook_openai_integration.py
```

Or use the launcher:

```bash
python run.py
```

## What Happens Next

1. The integration will scan your inbox every 15 minutes
2. For each unread email, it generates a professional draft response
3. Drafts are created in your Outlook Drafts folder
4. Processed emails are marked as read

## Troubleshooting

### "Authentication failed"
- Check your Azure App Registration credentials
- Ensure admin consent was granted for permissions

### "No emails processed"
- Check if emails are actually unread
- Verify domain filtering settings

### "OpenAI API error"
- Verify your OpenAI API key
- Check your OpenAI account balance

## Need Help?

1. Check the logs: `tail -f outlook_openai.log`
2. Run tests: `python test_setup.py`
3. See full documentation: `README.md`

## Configuration Options

Edit these in your `.env` file:

- `SCAN_INTERVAL_MINUTES=15` - How often to check emails
- `MAX_EMAILS_PER_SCAN=10` - Max emails per cycle
- `ALLOWED_DOMAINS=example.com` - Filter by sender domain
- `EMAIL_FOLDER=Inbox` - Which folder to monitor

That's it! Your AI email assistant is ready to go! 🚀 