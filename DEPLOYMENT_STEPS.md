# Deployment Steps

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click "New repository" (green button)
3. Repository name: `outlook-openai-integration`
4. Description: `Automated email response system with AI training`
5. Make it **Public** (so Vercel can access it)
6. Don't initialize with README (we already have one)
7. Click "Create repository"

## Step 2: Connect Local Repository

After creating the GitHub repository, you'll get a URL like:
`https://github.com/yourusername/outlook-openai-integration.git`

Run these commands (replace with your actual GitHub URL):

```bash
git remote add origin https://github.com/yourusername/outlook-openai-integration.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository (`outlook-openai-integration`)
4. Configure the project:
   - **Framework Preset**: `Other`
   - **Root Directory**: `./`
   - **Build Command**: `echo "No build required"`
   - **Output Directory**: `./`
   - **Install Command**: `pip install -r requirements.txt`

## Step 4: Add Environment Variables

In your Vercel project settings:

1. Go to **Project Settings** → **Environment Variables**
2. Add these variables:

```
CLIENT_ID=your_azure_app_client_id
CLIENT_SECRET=your_azure_app_client_secret
TENANT_ID=your_azure_tenant_id
OPENAI_API_KEY=your_openai_api_key
DAYS_THRESHOLD=4
ALLOWED_DOMAINS=example.com,company.com
```

## Step 5: Deploy

Click "Deploy" and wait for the deployment to complete.

## Step 6: Test the Deployment

1. Go to your Vercel project dashboard
2. Click on the **Functions** tab
3. Find `/api/outlook_openai` function
4. Click on it to view logs and test

## Step 7: Set Up Cron Job

The cron job is already configured in `cron.json` and will run every 6 hours automatically.

## Next Steps

After deployment:
1. Test the system with real emails
2. Start training the AI (see TRAINING_GUIDE.md)
3. Monitor logs for any issues
4. Customize responses based on your needs

## Troubleshooting

If deployment fails:
1. Check that all environment variables are set
2. Verify your Azure App Registration is configured correctly
3. Ensure your OpenAI API key is valid
4. Check Vercel function logs for specific errors 