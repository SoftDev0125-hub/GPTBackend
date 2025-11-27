# Railway Deployment - Step by Step

## Prerequisites

- ✅ Your code is ready (all files in place)
- ✅ GitHub account
- ✅ Railway account (free tier works)

## Step 1: Prepare Your Code for GitHub

### If you don't have a GitHub repo yet:

1. **Initialize Git (if not done):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - GPT Backend API"
   ```

2. **Create GitHub Repository:**
   - Go to https://github.com/new
   - Create a new repository (name it `gpt-backend` or similar)
   - Don't initialize with README (you already have files)

3. **Push Your Code:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git branch -M main
   git push -u origin main
   ```

### Important: Don't commit sensitive files!

Make sure `.gitignore` includes:
- `credentials.json`
- `token.json`
- `.env`

These will be uploaded separately to Railway.

## Step 2: Create Railway Account & Project

1. **Sign Up:**
   - Go to https://railway.app
   - Click "Start a New Project"
   - Sign up with GitHub (easiest)

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub
   - Select your repository (`gpt-backend` or whatever you named it)

3. **Railway Auto-Detection:**
   - Railway will detect Python automatically
   - It will read `requirements.txt` and install dependencies
   - It will use `Procfile` to start your app

## Step 3: Configure Environment

1. **In Railway Dashboard:**
   - Click on your service/project
   - Go to "Variables" tab

2. **Add Environment Variables (if needed):**
   - `GOOGLE_CREDENTIALS_PATH=credentials.json` (default, usually not needed)
   - `GOOGLE_TOKEN_PATH=token.json` (default, usually not needed)
   - `PORT` is automatically set by Railway

## Step 4: Upload Credentials

**Option A: Using Railway Files (Recommended)**

1. In Railway dashboard, go to your service
2. Click "Files" or "Settings" → "Files"
3. Upload `credentials.json` to the root directory
4. Upload `token.json` to the root directory (if you have it)

**Option B: Using Environment Variables**

1. Go to "Variables" tab
2. Create variable: `GOOGLE_CREDENTIALS` (paste entire JSON content)
3. Modify your code to read from env var instead of file

**Option C: Re-authenticate After Deployment**

1. After deployment, visit: `https://your-app.railway.app/gmail/auth/url`
2. Complete OAuth flow again
3. Token will be saved on Railway

## Step 5: Deploy

1. **Automatic Deploy:**
   - Railway automatically deploys when you push to GitHub
   - Or click "Deploy" button in Railway dashboard

2. **Watch the Logs:**
   - Click on your service
   - Go to "Deployments" tab
   - Watch the build process
   - Wait for "Deploy Successful"

3. **Get Your Public URL:**
   - In Railway dashboard, click on your service
   - Find "Public URL" or "Generate Domain"
   - Copy the URL: `https://your-app-name.up.railway.app`

## Step 6: Verify Deployment

Test your deployed API:

```bash
# Health check
curl https://your-app-name.up.railway.app/health

# OpenAPI schema
curl https://your-app-name.up.railway.app/openapi.json

# API docs
# Open in browser: https://your-app-name.up.railway.app/docs
```

## Step 7: Update Gmail Authentication (if needed)

If you uploaded `token.json`, it should work. Otherwise:

1. Visit: `https://your-app-name.up.railway.app/gmail/auth/url`
2. Copy the authorization URL
3. Complete OAuth flow
4. Use the callback endpoint to complete authentication

## Troubleshooting

### Build Fails
- Check Railway logs for errors
- Ensure `requirements.txt` is correct
- Verify `Procfile` exists and is correct

### 404 Errors
- Check that service is running
- Verify the URL is correct
- Check Railway logs for errors

### Gmail Authentication Fails
- Ensure `credentials.json` is uploaded
- Re-authenticate using Railway URL
- Check Railway logs for auth errors

### Port Issues
- Railway sets `PORT` automatically
- Your `Procfile` should use `${PORT}` variable
- Check that uvicorn is configured correctly

## Next Steps

Once deployed and working:

1. ✅ Test all endpoints via the public URL
2. ✅ Verify Gmail authentication works
3. ✅ Use the Railway URL in ChatGPT Assistant setup
4. ✅ Connect to ChatGPT (see `CONNECT_CHATGPT.md`)

## Railway URL Format

Your URL will look like:
```
https://gpt-backend-production-xxxx.up.railway.app
```

Use this URL for:
- OpenAPI schema: `https://your-url/openapi.json`
- Health check: `https://your-url/health`
- All API endpoints

---

**Need Help?** Check Railway logs in the dashboard for detailed error messages.

