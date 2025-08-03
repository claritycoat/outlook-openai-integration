# Outlook-OpenAI Integration

Automatically scan your Outlook emails and generate draft responses using OpenAI's GPT-4. This integration monitors your inbox for new emails, processes them with AI, and creates professional draft responses in your Drafts folder.

## Features

- 🔄 **Automatic Email Scanning**: Monitors your Outlook inbox for ALL emails up to 4 days old that haven't been replied to
- 🤖 **AI-Powered Responses**: Uses OpenAI GPT-4 to generate professional draft responses
- 📝 **Smart Draft Creation**: Creates drafts in your Outlook Drafts folder
- ⏰ **24/7 Serverless Operation**: Runs on Vercel regardless of your MacBook's status
- 🎓 **Training System**: Teach the AI your writing style and preferences
- 🔒 **Domain Filtering**: Optionally filter emails by sender domain
- 📊 **Comprehensive Logging**: Detailed logs for monitoring and debugging

## Prerequisites

- Python 3.8 or higher
- Microsoft 365 account with Outlook
- OpenAI API key
- Azure App Registration (for Microsoft Graph API access)

## Quick Start

### Option 1: Local Development
1. **Clone or download this project**
2. **Run the setup script**:
   ```bash
   python setup.py
   ```
3. **Configure your credentials** (see setup instructions below)
4. **Run the integration**:
   ```bash
   python outlook_openai_integration.py
   ```

### Option 2: Serverless Deployment (Recommended)
1. **Follow the deployment guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
2. **Deploy to Vercel** for 24/7 operation
3. **Train your AI**: [TRAINING_GUIDE.md](TRAINING_GUIDE.md)

## Detailed Setup Instructions

### 1. Microsoft Azure App Registration

You need to create an Azure App Registration to access Microsoft Graph API:

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to "Azure Active Directory" → "App registrations"
3. Click "New registration"
4. Fill in the details:
   - **Name**: "Outlook-OpenAI Integration"
   - **Supported account types**: "Accounts in this organizational directory only"
   - **Redirect URI**: (leave blank for now)
5. Click "Register"
6. Note down the **Application (client) ID** and **Directory (tenant) ID**

#### Configure API Permissions

1. In your app registration, go to "API permissions"
2. Click "Add a permission"
3. Select "Microsoft Graph"
4. Choose "Application permissions"
5. Add these permissions:
   - `Mail.Read`
   - `Mail.ReadWrite`
   - `Mail.Send`
6. Click "Grant admin consent" (requires admin privileges)

#### Create Client Secret

1. Go to "Certificates & secrets"
2. Click "New client secret"
3. Add a description and choose expiration
4. **Important**: Copy the secret value immediately (you won't see it again)

### 2. OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign in or create an account
3. Go to "API Keys"
4. Create a new API key
5. Copy the key (starts with `sk-`)

### 3. Environment Configuration

Edit the `.env` file with your credentials:

```env
# Microsoft Graph API Configuration
CLIENT_ID=your_azure_app_client_id
CLIENT_SECRET=your_azure_app_client_secret
TENANT_ID=your_tenant_id

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Email Processing Configuration
EMAIL_FOLDER=Inbox
PROCESSED_FOLDER=Drafts
SCAN_INTERVAL_MINUTES=15
MAX_EMAILS_PER_SCAN=10

# Optional: Filter emails by sender domain
ALLOWED_DOMAINS=example.com,company.com
```

### 4. Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `EMAIL_FOLDER` | Outlook folder to monitor | `Inbox` |
| `PROCESSED_FOLDER` | Folder for created drafts | `Drafts` |
| `SCAN_INTERVAL_MINUTES` | How often to check for new emails | `15` |
| `MAX_EMAILS_PER_SCAN` | Maximum emails to process per cycle | `10` |
| `ALLOWED_DOMAINS` | Comma-separated list of allowed sender domains | (all domains) |

## Usage

### Local Development

```bash
python outlook_openai_integration.py
```

The script will:
1. Authenticate with Microsoft Graph API
2. Scan your inbox for ALL emails up to 4 days old that haven't been replied to
3. Generate AI-powered responses (immediate for new emails, with delay acknowledgment for older emails)
4. Create drafts in your Drafts folder
5. Mark processed emails as read
6. Repeat the process every 15 minutes (configurable)

### Serverless Deployment

Once deployed to Vercel:
1. **Runs automatically** every 6 hours via cron job
2. **Processes ALL emails** up to 4 days old that haven't been replied to
3. **Creates immediate drafts** for new emails, with delay acknowledgment for older emails
4. **Uses your training data** for personalized responses
5. **Works 24/7** regardless of your MacBook's status

### Training Your AI

```bash
python training_system.py
```

Teach the AI your writing style:
1. Add examples of your best email responses
2. Create templates for common scenarios
3. Test and refine the responses
4. Deploy updated training data to Vercel

### Running as a Service

To run the integration as a background service on macOS:

1. Create a launch agent plist file:
```bash
mkdir -p ~/Library/LaunchAgents
```

2. Create `~/Library/LaunchAgents/com.outlook.openai.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.outlook.openai</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/justin/outlook-openai-integration/outlook_openai_integration.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/justin/outlook-openai-integration/outlook_openai.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/justin/outlook-openai-integration/outlook_openai.log</string>
</dict>
</plist>
```

3. Load the service:
```bash
launchctl load ~/Library/LaunchAgents/com.outlook.openai.plist
```

## How It Works

1. **Authentication**: Uses Azure App Registration to authenticate with Microsoft Graph API
2. **Email Scanning**: Periodically checks your inbox for unread emails
3. **AI Processing**: Sends email content to OpenAI GPT-4 for response generation
4. **Draft Creation**: Creates professional draft responses in your Drafts folder
5. **Status Tracking**: Marks processed emails as read to avoid reprocessing

## Security Considerations

- Store your `.env` file securely and never commit it to version control
- Use strong, unique client secrets for Azure App Registration
- Regularly rotate your OpenAI API key
- Consider using domain filtering to limit which emails are processed
- Monitor the logs for any unusual activity

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify your Azure App Registration credentials
   - Ensure API permissions are granted
   - Check that admin consent was given

2. **No Emails Processed**
   - Check if emails are actually unread
   - Verify domain filtering settings
   - Check logs for specific error messages

3. **OpenAI API Errors**
   - Verify your OpenAI API key
   - Check your OpenAI account balance
   - Ensure you're using a supported model

### Logs

The integration creates detailed logs in `outlook_openai.log`. Check this file for:
- Authentication status
- Email processing details
- Error messages
- Performance metrics

## Customization

### Modifying Response Generation

Edit the `generate_draft_response` method in `OpenAIHandler` class to customize:
- Response tone and style
- Response length
- Specific instructions for different email types

### Adding Email Filters

Modify the `should_process_email` method to add custom filtering logic:
- Email size limits
- Specific sender patterns
- Content-based filtering

## Support

For issues and questions:
1. Check the logs in `outlook_openai.log`
2. Verify your configuration in `.env`
3. Test your Azure App Registration permissions
4. Ensure your OpenAI API key is valid

## License

This project is provided as-is for educational and personal use. Please ensure compliance with Microsoft Graph API and OpenAI usage terms. 