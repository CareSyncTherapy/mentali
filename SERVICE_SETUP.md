# CareSync Service Setup Guide

This guide will walk you through setting up all the required services for CareSync.

## 🚀 Quick Setup Checklist

- [ ] Supabase (Database)
- [ ] Upstash (Redis)
- [ ] SendGrid (Email)
- [ ] Cloudinary (File Storage)
- [ ] Sentry (Error Tracking)
- [ ] Google Analytics
- [ ] Vercel (Frontend Hosting)
- [ ] Railway (Backend Hosting)

---

## 1. Supabase Setup (Database)

### Step 1: Create Account
1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign up with GitHub/Google
4. Create new organization: "CareSync"

### Step 2: Create Project
1. Click "New Project"
2. **Project Name**: `caresync-prod`
3. **Database Password**: Generate a strong password (save it!) - MentalHealth7!$
4. **Region**: Choose closest to your users
5. Click "Create new project"

### Step 3: Get Connection Details
1. Go to Settings → Database
2. Copy the connection string
3. Update `backend/.env`:


### Step 4: Create Database Tables
Run this SQL in Supabase SQL Editor:

```sql
-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('therapist', 'patient')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    language_preference VARCHAR(2) DEFAULT 'he',
    phone_number VARCHAR(20),
    profile_completed BOOLEAN DEFAULT FALSE
);

-- Create therapist_profiles table
CREATE TABLE therapist_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    experience_years INTEGER NOT NULL,
    education TEXT,
    languages JSONB,
    availability JSONB,
    hourly_rate DECIMAL(10,2),
    bio TEXT,
    verified BOOLEAN DEFAULT FALSE,
    rating DECIMAL(3,2) DEFAULT 0.0,
    total_reviews INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create patient_profiles table
CREATE TABLE patient_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(20),
    location VARCHAR(100),
    therapy_history TEXT,
    preferences JSONB,
    emergency_contact VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_therapist_profiles_specialization ON therapist_profiles(specialization);
CREATE INDEX idx_therapist_profiles_verified ON therapist_profiles(verified);
```

---

## 2. Upstash Setup (Redis)

### Step 1: Create Account
1. Go to [upstash.com](https://upstash.com)
2. Click "Get Started"
3. Sign up with GitHub/Google

### Step 2: Create Database
1. Click "Create Database"
2. **Name**: `caresync-redis`
3. **Region**: Choose closest to your backend
4. **TLS**: Enabled
5. Click "Create"

### Step 3: Get Connection Details
1. Copy the connection string
2. Update `backend/.env`:

```env
REDIS_URL=redis://default:[YOUR-PASSWORD]@[YOUR-REGION].upstash.io:6379
RATELIMIT_STORAGE_URL=redis://default:[YOUR-PASSWORD]@[YOUR-REGION].upstash.io:6379
```

---

## 3. Resend Setup (Email)

### Step 1: Create Account
1. Go to [resend.com](https://resend.com)
2. Click "Get Started"
3. Sign up with GitHub/Google (no SMS required)
4. Verify your email address

### Step 2: Skip Domain Setup (For Now)
1. You can use Resend's default domain for testing
2. **From Email**: `onboarding@resend.dev`
3. **Later**: Add your own domain when you have one
# Instructions for later:
# Buy a domain (Namecheap, GoDaddy, etc.)
# Add it to Resend (Domains tab)
# Follow DNS instructions (like you saw)
# Update your .env to use your domain

### Step 3: Create API Key
1. Go to API Keys tab
2. Click "Create API Key"
3. **API Key Name**: CareSync API
4. **Permissions**: Full Access
5. Click "Create"
6. Copy the API key

### Step 4: Update Environment
Update `backend/.env`:

```env
# Email Configuration - Resend
RESEND_API_KEY=re_[YOUR-RESEND-API-KEY]
EMAIL_FROM=onboarding@resend.dev
EMAIL_REPLY_TO=support@caresync.com
```

---

## 4. Cloudinary Setup (File Storage)

### Step 1: Create Account
1. Go to [cloudinary.com](https://cloudinary.com)
2. Click "Sign Up For Free"
3. Sign up with email

### Step 2: Get Credentials
1. Go to Dashboard
2. Copy your credentials:
   - Cloud Name
   - API Key
   - API Secret

### Step 3: Update Environment
Update `backend/.env`:

```env
CLOUDINARY_CLOUD_NAME=caresync
CLOUDINARY_API_KEY=[YOUR-CLOUDINARY-API-KEY]
CLOUDINARY_API_SECRET=[YOUR-CLOUDINARY-API-SECRET]
```

---

## 5. Sentry Setup (Error Tracking)

### Step 1: Create New Account with Email Alias
1. Go to [sentry.io](https://sentry.io)
2. **Sign out** if you're logged in
3. Click "Get Started"
4. **Use email alias**: `dansashadan+caresync@gmail.com`
5. **Create new password**
6. **Don't join existing organization** when prompted

### Step 2: Create Organization & Project
1. **Organization Name**: `CareSync`
2. **Team Name**: `Development`
3. Click "Create Project"
4. **Platform**: Python
5. **Project Name**: `caresync-backend`
6. Click "Create Project"

### Step 3: Get DSN
1. Copy the DSN string
2. Update `backend/.env`:

```env
SENTRY_DSN=https://[YOUR-SENTRY-DSN]@[YOUR-ORG].ingest.sentry.io/[YOUR-PROJECT]
```

---

## 6. Google Analytics Setup

### Step 1: Create Account
1. Go to [analytics.google.com](https://analytics.google.com)
2. Click "Start measuring"
3. Sign in with Google account

### Step 2: Create Property
1. Click "Create Property"
2. **Property Name**: CareSync
3. **Reporting Time Zone**: Your timezone
4. **Currency**: USD
5. Click "Next"

### Step 3: Get Tracking ID
1. Copy the Measurement ID (G-XXXXXXXXXX)
2. Update `backend/.env`:

```env
GOOGLE_ANALYTICS_ID=G-[YOUR-GA-ID]
```

---

## 7. Vercel Setup (Frontend Hosting)

### Step 1: Transfer Repository
1. **Go to your `mentali` repo** on GitHub
2. **Settings** → **Danger Zone**
3. **Click "Transfer ownership"**
4. **New owner**: `CareSyncTherapy`
5. **Confirm transfer**

### Step 2: Make Organization Public
1. **Go to your `CareSyncTherapy` organization**
2. **Settings** → **General**
3. **Change visibility** from "Private" to "Public"
4. **Confirm the change**

### Step 3: Connect Organization to Vercel
1. Go to [vercel.com](https://vercel.com)
2. **Sign in** with your GitHub account
3. **Add GitHub organization**: `CareSyncTherapy`
4. **Authorize** the organization
5. **Import the transferred repo**
6. **Framework Preset**: Vite
7. **Root Directory**: `frontend-web`
8. **Project Name**: `caresync-frontend`
9. Click "Deploy"

### Step 3: Configure Environment Variables
1. Go to Project Settings → Environment Variables
2. Add:
   ```
   VITE_API_URL=https://your-backend-url.railway.app/api
   VITE_APP_VERSION=1.0.0
   ```

---

## 8. Railway Setup (Backend Hosting)

### Step 1: Create Account
1. Go to [railway.app](https://railway.app)
2. Click "Deploy Now"
3. Sign up with GitHub

### Step 2: Create Project
1. Click "New Project"
2. **Deploy from GitHub repo**
3. Select your repository
4. **Root Directory**: `backend`

### Step 3: Configure Environment Variables
1. Go to Variables tab
2. Add all variables from `backend/.env`
3. Set `APP_ENVIRONMENT=production`

---

## 9. Final Configuration

### Update App Name
Replace all instances of "INNERA" with "CareSync" in:
- `backend/main.py`
- `frontend-web/src/App.tsx`
- `frontend-web/index.html`
- All documentation files

### Generate Secure Keys
```bash
# Generate secret keys
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Update these in `backend/.env`:
```env
SECRET_KEY=your-generated-secret-key
JWT_SECRET_KEY=your-generated-jwt-secret-key
```

---

## 10. Test All Services

### Test Database
```bash
cd backend
python -c "
from main import app, db
with app.app_context():
    db.create_all()
    print('Database connection successful!')
"
```

### Test Email
```bash
# Test SendGrid connection
curl -X POST https://api.sendgrid.com/v3/mail/send \
  -H "Authorization: Bearer YOUR_SENDGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"personalizations":[{"to":[{"email":"test@example.com"}]}],"from":{"email":"noreply@caresync.com"},"subject":"Test","content":[{"type":"text/plain","value":"Test email"}]}'
```

### Test File Upload
```bash
# Test Cloudinary upload
curl -X POST https://api.cloudinary.com/v1_1/caresync/image/upload \
  -F "file=@test.jpg" \
  -F "api_key=YOUR_API_KEY" \
  -F "timestamp=$(date +%s)"
```

---

## 11. Deployment Checklist

- [ ] All environment variables set
- [ ] Database tables created
- [ ] Email service configured
- [ ] File storage configured
- [ ] Error tracking enabled
- [ ] Analytics tracking enabled
- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Railway
- [ ] Custom domain configured (optional)
- [ ] SSL certificates active
- [ ] Health checks passing

---

## 12. Monitoring Setup

### Set up alerts for:
- Database connection failures
- Email delivery failures
- API response time > 2s
- Error rate > 5%
- Disk space > 80%

### Regular maintenance:
- Weekly database backups
- Monthly security updates
- Quarterly performance reviews

---

## Cost Summary

**Development (FREE)**:
- Supabase: $0/month
- Upstash: $0/month
- SendGrid: $0/month
- Cloudinary: $0/month
- Sentry: $0/month
- Vercel: $0/month
- Railway: $0/month

**Production (Recommended)**:
- Supabase Pro: $25/month
- SendGrid Pro: $15/month
- Railway Pro: $20/month
- Vercel Pro: $20/month
- Sentry Pro: $26/month
- **Total**: ~$106/month

---

## Support

If you encounter issues:
1. Check service status pages
2. Review error logs
3. Contact service support
4. Check our troubleshooting guide

**Happy coding! 🚀** 