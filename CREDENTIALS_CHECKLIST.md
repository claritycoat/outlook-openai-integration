# Credentials Checklist

Before deploying to Vercel, make sure you have all these credentials ready:

## ✅ Microsoft Azure App Registration

### Required Credentials:
- [ ] **CLIENT_ID** (Application ID from Azure App Registration)
- [ ] **CLIENT_SECRET** (Secret value from Azure App Registration)
- [ ] **TENANT_ID** (Directory ID from Azure App Registration)

### Setup Steps:
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to "Azure Active Directory" → "App registrations"
3. Click "New registration"
4. Name: "Outlook-OpenAI Integration"
5. Account types: "Accounts in this organizational directory only"
6. Click "Register"
7. Copy the **Application (client) ID** and **Directory (tenant) ID**

### API Permissions:
1. Go to "API permissions" → "Add a permission"
2. Select "Microsoft Graph" → "Application permissions"
3. Add these permissions:
   - [ ] `Mail.Read`
   - [ ] `Mail.ReadWrite`
   - [ ] `Mail.Send`
4. Click "Grant admin consent"

### Create Client Secret:
1. Go to "Certificates & secrets"
2. Click "New client secret"
3. Add description and choose expiration
4. **Copy the secret value immediately** (you won't see it again)

## ✅ OpenAI API Key

### Required Credentials:
- [ ] **OPENAI_API_KEY** (starts with `sk-`)

### Setup Steps:
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create account
3. Go to "API Keys"
4. Create new API key
5. Copy the key (starts with `sk-`)

## ✅ Optional Configuration

### Environment Variables:
- [ ] **DAYS_THRESHOLD** (set to `4` for 4-day processing)
- [ ] **ALLOWED_DOMAINS** (optional, comma-separated list)

## ✅ Test Your Credentials

Before deploying, test your credentials locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Test the setup
python test_setup.py
```

This will verify that all your credentials are working correctly.

## ✅ Deployment Ready

Once you have all credentials:
1. Create GitHub repository
2. Push code to GitHub
3. Deploy to Vercel
4. Add environment variables in Vercel dashboard
5. Test the deployment

## 🔧 Troubleshooting

### Common Issues:
- **Authentication failed**: Check Azure App Registration credentials
- **API permissions error**: Ensure admin consent was granted
- **OpenAI API error**: Verify API key and account balance
- **No emails processed**: Check if emails are actually up to 4 days old

### Getting Help:
1. Check Vercel function logs
2. Run `python test_setup.py` locally
3. Verify all environment variables are set correctly
4. Ensure Azure App Registration has correct permissions 