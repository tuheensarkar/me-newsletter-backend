# Quick Start: Testing Lovable Integration

## Immediate Testing Steps

### 1. Test Current Django Backend

```bash
# Navigate to project directory
cd ME-Newsletter-BE-news_ltr\ME-Newsletter-BE-news_ltr

# Create virtual environment (if not exists)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements\local.txt

# Run development server
python manage.py runserver
```

### 2. Test New API Endpoints

Open your browser and test these URLs:

1. **Health Check**: http://127.0.0.1:8000/api/health/
2. **API Status**: http://127.0.0.1:8000/api/status/
3. **Newsletter List**: http://127.0.0.1:8000/api/v1/newsletters/
4. **Recent Newsletters**: http://127.0.0.1:8000/api/v1/newsletters/recent/
5. **API Documentation**: http://127.0.0.1:8000/api/docs/

Expected responses:
- Health check should return JSON with database status
- API status should confirm service is operational
- Newsletter endpoints should return data or empty arrays

### 3. Test CORS Configuration

Use curl to test CORS headers:
```bash
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS \
     http://127.0.0.1:8000/api/v1/newsletters/
```

Should return appropriate CORS headers allowing localhost:3000

### 4. Create Test Data (Optional)

```bash
# Create superuser
python manage.py createsuperuser

# Access admin panel
# Go to http://127.0.0.1:8000/admin/
# Create sample newsletters and test data
```

### 5. Test Subscription Endpoint

Using curl:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/subscribe/ \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com"}'
```

Should return success message with 201 status.

## Lovable Frontend Setup

### 1. Create Lovable Project
1. Go to https://lovable.dev
2. Create new Next.js project
3. Connect to your GitHub repository

### 2. Configure Environment Variables
In Lovable dashboard:
```
NEXT_PUBLIC_API_URL=http://your-go daddy-domain.com/api/v1/
NEXT_PUBLIC_SITE_URL=https://your-app.lovable.dev
```

### 3. Deploy Test Version
1. Push the frontend code to GitHub
2. Lovable will automatically deploy
3. Test API connectivity from deployed frontend

## Troubleshooting

### Common Issues:

**API Connection Refused:**
- Ensure Django server is running
- Check firewall settings
- Verify GoDaddy allows external connections

**CORS Errors:**
- Check CORS configuration in settings.py
- Verify allowed origins include your Lovable domain
- Test with different browsers

**Database Connection:**
- Verify database credentials
- Check GoDaddy database accessibility
- Test connection with pgAdmin or psql

### Logs to Check:
- Django development server output
- Browser developer console
- Lovable deployment logs
- GoDaddy application logs

## Success Criteria

✅ Health check endpoint returns 200 OK
✅ Newsletter API returns data (even if empty)
✅ CORS headers are present for localhost
✅ Subscription endpoint accepts POST requests
✅ API documentation loads properly

Once these tests pass, you're ready to proceed with full Lovable integration.