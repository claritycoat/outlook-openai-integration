# Azure Setup Checklist

## ✅ Step-by-Step Checklist

### Step 1: Access Azure Portal
- [ ] Go to [Azure Portal](https://portal.azure.com)
- [ ] Sign in with your Azure account
- [ ] Dashboard loads successfully

### Step 2: Navigate to App Registrations
- [ ] Type "App registrations" in search bar
- [ ] Click on "App registrations" in results
- [ ] See the App registrations page

### Step 3: Create New App Registration
- [ ] Click "New registration" button
- [ ] Fill in the form:
  - [ ] Name: `Outlook-OpenAI Integration`
  - [ ] Supported account types: `Accounts in this organizational directory only`
  - [ ] Redirect URI: Leave blank
- [ ] Click "Register"

### Step 4: Get Application ID and Tenant ID
- [ ] Copy **Application (client) ID** → This is your `CLIENT_ID`
- [ ] Copy **Directory (tenant) ID** → This is your `TENANT_ID`

### Step 5: Add API Permissions
- [ ] Click "API permissions" in left sidebar
- [ ] Click "Add a permission"
- [ ] Select "Microsoft Graph"
- [ ] Choose "Application permissions" (not Delegated)
- [ ] Search and select these permissions:
  - [ ] `Mail.Read`
  - [ ] `Mail.ReadWrite`
  - [ ] `Mail.Send`
- [ ] Click "Add permissions"
- [ ] Click "Grant admin consent"

### Step 6: Create Client Secret
- [ ] Click "Certificates & secrets" in left sidebar
- [ ] Click "New client secret"
- [ ] Add description: `Outlook-OpenAI Integration Secret`
- [ ] Choose expiration (e.g., 12 months)
- [ ] Click "Add"
- [ ] **IMPORTANT**: Copy the secret value immediately → This is your `CLIENT_SECRET`

## ✅ Your Credentials Summary

After completing all steps, you should have:

| Credential | Value Format | Where to Find |
|------------|--------------|---------------|
| **CLIENT_ID** | `12345678-1234-1234-1234-123456789012` | Application (client) ID |
| **CLIENT_SECRET** | `abc123def456ghi789...` | Secret value (copy immediately) |
| **TENANT_ID** | `87654321-4321-4321-4321-210987654321` | Directory (tenant) ID |

## ✅ Test Your Setup

Once you have all three values:

```bash
# Create .env file with your credentials
echo "CLIENT_ID=your_client_id_here" > .env
echo "CLIENT_SECRET=your_client_secret_here" >> .env
echo "TENANT_ID=your_tenant_id_here" >> .env

# Test the setup
python test_setup.py
```

## ❌ Common Issues & Solutions

### Issue: "You don't have permission to grant admin consent"
**Solution**: Contact your Azure administrator or use a personal Microsoft account

### Issue: "No API permissions found"
**Solution**: Make sure you selected "Application permissions" (not Delegated)

### Issue: "Secret not showing"
**Solution**: You can only see it once. Delete old secret and create new one

### Issue: "Authentication failed"
**Solution**: Double-check all three values are copied correctly

## 🚀 Next Steps

After completing Azure setup:

1. **Get OpenAI API key** (see AZURE_SETUP_GUIDE.md)
2. **Create GitHub repository**
3. **Deploy to Vercel**
4. **Add environment variables**
5. **Test deployment**

## 📞 Need Help?

If you get stuck:
1. Check the detailed guide: `AZURE_SETUP_GUIDE.md`
2. Run `python test_setup.py` to verify credentials
3. Check Vercel function logs for specific errors
4. Ensure all permissions are granted correctly 