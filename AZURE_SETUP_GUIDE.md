# Azure App Registration Setup Guide

## Step-by-Step Instructions

### Step 1: Access Azure Portal

1. **Go to [Azure Portal](https://portal.azure.com)**
2. **Sign in** with your Azure account
3. **Wait for the dashboard to load**

### Step 2: Navigate to App Registrations

1. **In the search bar at the top**, type: `App registrations`
2. **Click on "App registrations"** in the search results
3. **You should see a page titled "App registrations"**

### Step 3: Create New App Registration

1. **Click the "New registration" button** (usually a blue button)
2. **Fill in the registration form**:
   - **Name**: `Outlook-OpenAI Integration`
   - **Supported account types**: Select `Accounts in this organizational directory only`
   - **Redirect URI**: Leave this blank for now
3. **Click "Register"** at the bottom

### Step 4: Get Your Application ID and Tenant ID

After registration, you'll be taken to the app overview page. **Copy these values**:

1. **Application (client) ID**: This is your `CLIENT_ID`
   - It looks like: `12345678-1234-1234-1234-123456789012`
   - Copy this value

2. **Directory (tenant) ID**: This is your `TENANT_ID`
   - It looks like: `87654321-4321-4321-4321-210987654321`
   - Copy this value

### Step 5: Add API Permissions

1. **In the left sidebar**, click on **"API permissions"**
2. **Click "Add a permission"** button
3. **Select "Microsoft Graph"** from the list
4. **Choose "Application permissions"** (not Delegated)
5. **Search for and select these permissions**:
   - `Mail.Read`
   - `Mail.ReadWrite`
   - `Mail.Send`
6. **Click "Add permissions"**
7. **Click "Grant admin consent"** (this requires admin privileges)
   - If you're not an admin, you may need to contact your Azure admin

### Step 6: Create Client Secret

1. **In the left sidebar**, click on **"Certificates & secrets"**
2. **Click "New client secret"**
3. **Add a description**: `Outlook-OpenAI Integration Secret`
4. **Choose expiration**: Select an appropriate duration (e.g., 12 months)
5. **Click "Add"**
6. **IMPORTANT**: Copy the secret value immediately
   - It looks like: `abc123def456ghi789...`
   - This is your `CLIENT_SECRET`
   - You won't be able to see it again after leaving this page

### Step 7: Verify Your Setup

You should now have these three values:

- ✅ **CLIENT_ID**: Application (client) ID
- ✅ **CLIENT_SECRET**: Secret value you just created
- ✅ **TENANT_ID**: Directory (tenant) ID

## Troubleshooting

### Common Issues:

1. **"You don't have permission to grant admin consent"**
   - Contact your Azure administrator
   - Or use a personal Microsoft account for testing

2. **"No API permissions found"**
   - Make sure you selected "Application permissions" (not Delegated)
   - Try searching for "Mail" in the permissions list

3. **"Secret not showing"**
   - You can only see the secret value once
   - If you missed it, delete the old secret and create a new one

### Testing Your Credentials:

Once you have all three values, you can test them locally:

```bash
# Create a .env file with your credentials
echo "CLIENT_ID=your_client_id_here" > .env
echo "CLIENT_SECRET=your_client_secret_here" >> .env
echo "TENANT_ID=your_tenant_id_here" >> .env

# Test the setup
python test_setup.py
```

## Next Steps

After completing the Azure setup:

1. **Get your OpenAI API key** (see next section)
2. **Create GitHub repository**
3. **Deploy to Vercel**
4. **Add all environment variables**

## OpenAI API Key Setup

1. **Go to [OpenAI Platform](https://platform.openai.com/api-keys)**
2. **Sign in or create account**
3. **Go to "API Keys"**
4. **Click "Create new secret key"**
5. **Copy the key** (starts with `sk-`)
6. **This is your `OPENAI_API_KEY`**

## Complete Environment Variables

Once you have all credentials, you'll need these for Vercel:

```
CLIENT_ID=your_azure_client_id
CLIENT_SECRET=your_azure_client_secret
TENANT_ID=your_azure_tenant_id
OPENAI_API_KEY=your_openai_api_key
DAYS_THRESHOLD=4
ALLOWED_DOMAINS=example.com,company.com
```

## Security Notes

- **Never commit your .env file** to version control
- **Store secrets securely** in Vercel environment variables
- **Rotate secrets regularly** for security
- **Use strong, unique secrets** for production

## Getting Help

If you encounter issues:

1. **Check Azure documentation**: [Microsoft Graph API](https://docs.microsoft.com/en-us/graph/)
2. **Verify permissions**: Make sure all three Mail permissions are granted
3. **Test locally**: Use `python test_setup.py` to verify credentials
4. **Check logs**: Vercel function logs will show specific errors 