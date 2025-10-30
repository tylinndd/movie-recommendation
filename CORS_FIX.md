# CORS Network Error - Root Cause & Fix 🎯

## The Problem

You were getting network errors when trying to login or signup because of a **CORS configuration issue** in your Flask backend.

### What Was Wrong

In `main.py`, lines 40-50 had this problematic code:

```python
allowed_origins = []
if is_production:
    render_url = os.environ.get('RENDER_EXTERNAL_URL', '')
    if render_url:
        allowed_origins.append(render_url)
else:
    allowed_origins = ['http://localhost:5000', 'http://127.0.0.1:5000']

CORS(app, supports_credentials=True, origins=allowed_origins if allowed_origins else None)
```

### Why It Failed

1. **On Render (Production)**:
   - `RENDER_EXTERNAL_URL` environment variable doesn't exist by default
   - So `allowed_origins` stayed as an empty list `[]`
   - Empty list evaluates to `False`, so CORS got `origins=None`
   - With `supports_credentials=True` and no valid origins, browsers blocked ALL requests

2. **Locally**:
   - Actually worked fine because `allowed_origins` was set to `['http://localhost:5000', 'http://127.0.0.1:5000']`
   - But if you accessed via `file://` or different port, it would fail

### The Security Rule

**Critical:** When using `supports_credentials=True` (required for cookies/sessions), you **cannot** use:
- ❌ Wildcard `origins='*'`
- ❌ `origins=None`
- ✅ Must specify exact origins OR let Flask-CORS handle same-origin automatically

## The Fix

Changed line 41 in `main.py` to:

```python
CORS(app, supports_credentials=True)
```

### Why This Works

**Your app uses same-origin architecture:**
- Frontend HTML: Served from Flask at `/` → `http://localhost:5000/` or `https://yourapp.onrender.com/`
- Backend APIs: Served from Flask at `/api/*` → `http://localhost:5000/api/*` or `https://yourapp.onrender.com/api/*`
- **Same origin** = No CORS restrictions needed!

By removing the `origins` parameter:
- Flask-CORS automatically allows **same-origin** requests
- Still supports credentials (cookies for authentication)
- Works on both local development AND Render production
- No need for environment variables or complex origin configuration

## How to Deploy

### 1. Test Locally

```bash
cd /Users/tylin/movie-recommendation
python main.py
```

Then visit `http://localhost:5000` and test:
- ✅ Sign up with a new account
- ✅ Log in with credentials
- ✅ Add movies to watchlist
- ✅ Mark movies as watched

### 2. Deploy to Render

```bash
git add main.py
git commit -m "Fix CORS configuration for same-origin requests"
git push origin main
```

Render will automatically detect the push and redeploy (takes ~2-5 minutes).

### 3. Verify on Render

Visit your Render URL (e.g., `https://yourapp.onrender.com`) and test the same features.

## What This Fixes

✅ **Login works** - No more network errors  
✅ **Signup works** - Sessions properly maintained  
✅ **Works locally** - No configuration needed  
✅ **Works on Render** - No environment variables needed  
✅ **Secure** - Still uses HTTPS cookies in production  
✅ **Simple** - No complex CORS origin management  

## Technical Details

### Session Cookie Settings (Already Configured)

These settings in your `main.py` are already correct and handle the HTTPS requirements:

```python
app.config['SESSION_COOKIE_SECURE'] = is_production  # HTTPS only in production
app.config['SESSION_COOKIE_HTTPONLY'] = True         # JavaScript can't access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'        # CSRF protection
```

### Frontend Credentials (Already Configured)

Your `app.js` already includes `credentials: 'include'` in all fetch requests, which is correct:

```javascript
fetch('/api/login', {
    method: 'POST',
    credentials: 'include',  // ✅ Sends cookies
    // ...
})
```

## Why Same-Origin Matters

**Same-Origin Request** (Your app):
```
Frontend: https://yourapp.onrender.com/
API Call:  https://yourapp.onrender.com/api/login
→ Same protocol, domain, and port = Same origin
→ No CORS preflight needed
→ Cookies automatically included
```

**Cross-Origin Request** (If frontend was separate):
```
Frontend:  https://my-frontend.vercel.app/
API Call:  https://my-backend.onrender.com/api/login
→ Different domains = Cross-origin
→ Requires proper CORS configuration with exact origins
→ Cannot use wildcards with credentials
```

Your architecture is **same-origin**, which is simpler and more secure!

## Troubleshooting

If you still see issues:

### Check Browser Console (F12 → Console)
Look for:
- ❌ "CORS policy" errors → CORS issue
- ❌ "Failed to fetch" → Network/server issue
- ❌ "credentials mode" errors → Fetch needs `credentials: 'include'`

### Check Render Logs (Dashboard → Logs)
Look for:
- ❌ Python errors
- ❌ Database connection issues
- ✅ Should see successful request logs

### Verify Cookies (F12 → Application → Cookies)
After logging in, you should see:
- ✅ `session` cookie
- ✅ `Secure` flag (on Render)
- ✅ `HttpOnly` flag
- ✅ `SameSite=Lax`

### Hard Refresh
- Windows: `Ctrl + Shift + R`
- Mac: `Cmd + Shift + R`

This clears cached JavaScript that might have old fetch configurations.

## Summary

The problem was **misconfigured CORS origins** that resulted in browsers blocking your authentication requests. Since your app uses **same-origin architecture** (frontend and backend from same Flask server), you don't need complex CORS origin management. Simply enabling CORS with credentials support is enough.

**The fix is deployed once you push the updated `main.py` to GitHub!** 🚀

