# Deploying PyCEFRL Streamlit App

This guide explains how to deploy the PyCEFRL Streamlit web application.

## Streamlit Cloud (Recommended)

The easiest way to deploy the Streamlit app is using [Streamlit Cloud](https://streamlit.io/cloud):

### Steps:

1. **Sign up for Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Sign in with your GitHub account

2. **Deploy the App**
   - Click "New app"
   - Select the repository: `raux/pycefrl`
   - Choose branch: `main`
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Configuration**
   - The app will automatically use `.streamlit/config.toml` for configuration
   - System dependencies in `packages.txt` will be installed automatically
   - Python dependencies from `requirements.txt` will be installed

### Expected Deployment Time
- Initial deployment: 3-5 minutes
- Subsequent updates: 1-2 minutes

### Public URL
Once deployed, you'll get a URL like: `https://your-app-name.streamlit.app`

## Alternative Deployment Options

### Docker Deployment

1. **Create a Dockerfile** (example):
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Generate dictionary file
RUN python3 dict.py

# Expose Streamlit port
EXPOSE 8501

# Run the app
CMD ["python3", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Build and run**:
```bash
docker build -t pycefrl-app .
docker run -p 8501:8501 pycefrl-app
```

### Heroku Deployment

1. **Create required files**:

`Procfile`:
```
web: sh setup.sh && python3 -m streamlit run app.py
```

`setup.sh`:
```bash
#!/bin/bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
python3 dict.py
```

2. **Deploy**:
```bash
heroku create your-app-name
git push heroku main
```

### Railway Deployment

1. **Connect GitHub repository** to [Railway](https://railway.app/)
2. **Configure**:
   - Add start command: `python3 dict.py && python3 -m streamlit run app.py --server.port=$PORT`
   - Railway will auto-detect `requirements.txt`

### Render Deployment

1. **Create a new Web Service** on [Render](https://render.com/)
2. **Configure**:
   - Build Command: `pip3 install -r requirements.txt && python3 dict.py`
   - Start Command: `python3 -m streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

## Environment Variables

No environment variables are required for basic deployment. However, if you want to configure GitHub API access for rate limiting:

- `GITHUB_TOKEN`: Personal access token for GitHub API (optional)

## Post-Deployment

After deployment, the web app will:
- ✅ Allow real-time analysis of local directories (if running locally)
- ✅ Analyze GitHub repositories by URL
- ✅ Analyze GitHub user profiles
- ✅ Display interactive visualizations
- ✅ Provide downloadable CSV/JSON reports

## Troubleshooting

### Issue: "Dictionary file not found"
**Solution**: Make sure `dict.py` runs during deployment. Add it to your build/start script.

### Issue: "Git command not found"
**Solution**: Ensure `git` is in `packages.txt` for Streamlit Cloud, or installed in Docker/Heroku.

### Issue: Memory errors on large repositories
**Solution**: Deploy on a platform with at least 1GB RAM. Streamlit Cloud provides sufficient resources.

## Monitoring

Once deployed, monitor:
- **Performance**: Response times for analysis
- **Errors**: Check logs for failed repository clones
- **Usage**: Track number of analyses performed

## Updating the Deployment

For Streamlit Cloud:
1. Push changes to GitHub
2. Streamlit Cloud auto-deploys from the connected branch

For other platforms:
1. Push changes to your repository
2. Trigger manual deployment or wait for auto-deploy

## Security Considerations

- The app clones public GitHub repositories - ensure appropriate rate limiting
- No authentication is required for public deployment
- Consider adding authentication for production use
- Repository clones are temporary and cleaned up after analysis

## Support

For deployment issues:
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [GitHub Issues](https://github.com/raux/pycefrl/issues)
