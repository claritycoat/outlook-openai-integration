# Vercel Deployment Guide

Deploy your Outlook-OpenAI integration to Vercel for 24/7 operation that creates draft responses for ALL emails up to 4 days old.

## Prerequisites

- Vercel account (free tier works)
- GitHub account (to connect your repository)
- All credentials from the setup process

## Step 1: Prepare for Deployment

1. **Create a GitHub repository** (if you haven't already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/outlook-openai-integration.git
   git push -u origin main
   ```

2. **Update environment variables** for serverless deployment:
   ```env
   # Microsoft Graph API Configuration
   CLIENT_ID=your_azure_app_client_id
   CLIENT_SECRET=your_azure_app_client_secret
   TENANT_ID=your_tenant_id
   
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key
   
   # Email Processing Configuration
   DAYS_THRESHOLD=4
   ALLOWED_DOMAINS=example.com,company.com
   ```

## Step 2: Deploy to Vercel

1. **Go to [Vercel Dashboard](https://vercel.com/dashboard)**
2. **Click "New Project"**
3. **Import your GitHub repository**
4. **Configure the project**:
   - Framework Preset: `Other`
   - Root Directory: `./`
   - Build Command: `echo "No build required"`
   - Output Directory: `./`
   - Install Command: `pip install -r requirements.txt`

5. **Add Environment Variables** in Vercel:
   - Go to Project Settings → Environment Variables
   - Add each variable from your `.env` file:
     - `CLIENT_ID`
     - `CLIENT_SECRET`
     - `TENANT_ID`
     - `OPENAI_API_KEY`
     - `DAYS_THRESHOLD` (set to `4`)
     - `ALLOWED_DOMAINS` (optional)

6. **Deploy the project**

## Step 3: Set Up Cron Job

### Option A: Vercel Cron (Recommended)

1. **Create a cron.json file** in your project root:
   ```json
   {
     "crons": [
       {
         "path": "/api/outlook_openai",
         "schedule": "0 */6 * * *"
       }
     ]
   }
   ```

2. **Deploy the cron configuration**:
   ```bash
   git add cron.json
   git commit -m "Add cron job configuration"
   git push
   ```

### Option B: External Cron Service

Use a service like [cron-job.org](https://cron-job.org) to hit your Vercel endpoint:

1. **Get your Vercel URL**: `https://your-project.vercel.app/api/outlook_openai`
2. **Set up cron job** to hit this URL every 6 hours
3. **Method**: POST

## Step 4: Test the Deployment

1. **Test the endpoint**:
   ```bash
   curl https://your-project.vercel.app/api/outlook_openai
   ```

2. **Check the response** - you should see JSON with processing results

## Step 5: Monitor and Debug

### View Logs
- Go to your Vercel project dashboard
- Click on "Functions" tab
- View the logs for your `/api/outlook_openai` function

### Test Locally
```bash
# Install Vercel CLI
npm i -g vercel

# Link your project
vercel link

# Run locally
vercel dev
```

## Configuration Options

### Cron Schedule Options

| Schedule | Frequency | Description |
|----------|-----------|-------------|
| `0 */6 * * *` | Every 6 hours | Good balance |
| `0 */4 * * *` | Every 4 hours | More frequent |
| `0 */12 * * *` | Every 12 hours | Less frequent |
| `0 9,18 * * *` | Twice daily (9 AM, 6 PM) | Business hours |

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DAYS_THRESHOLD` | Emails older than X days need replies | `4` |
| `ALLOWED_DOMAINS` | Comma-separated list of allowed domains | (all domains) |

## Troubleshooting

### Common Issues

1. **Function timeout**
   - Increase `maxDuration` in `vercel.json`
   - Reduce `$top` parameter in email queries

2. **Authentication errors**
   - Verify environment variables in Vercel dashboard
   - Check Azure App Registration permissions

3. **No emails processed**
   - Check if emails are actually older than threshold
   - Verify domain filtering settings

### Debugging

1. **Check Vercel function logs**:
   - Go to your project dashboard
   - Click "Functions" → `/api/outlook_openai`
   - View recent invocations

2. **Test locally**:
   ```bash
   vercel dev
   curl http://localhost:3000/api/outlook_openai
   ```

3. **Check environment variables**:
   ```bash
   vercel env ls
   ```

## Cost Considerations

- **Vercel Hobby Plan**: Free tier includes:
  - 100GB-hours of serverless function execution
  - 100GB bandwidth
  - Perfect for this use case

- **OpenAI API**: ~$0.03 per email processed
- **Estimated monthly cost**: $5-15 depending on email volume

## Security Notes

- Environment variables are encrypted in Vercel
- No need to commit `.env` file to repository
- Function logs are private to your account
- Consider using Vercel's team features for production

## Next Steps

1. **Deploy and test** the basic functionality
2. **Set up monitoring** with Vercel Analytics
3. **Customize response generation** (see next section)
4. **Add email templates** for different scenarios

Your integration will now run 24/7, creating draft responses for ALL emails up to 4 days old that haven't been replied to! 🚀 