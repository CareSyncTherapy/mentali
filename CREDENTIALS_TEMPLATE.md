# CareSync Service Credentials Template

This document contains all the credentials and configuration values needed for CareSync.

## 🔐 Backend Environment Variables

Create `backend/.env` with these values:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=[GENERATE-SECURE-KEY]
JWT_SECRET_KEY=[GENERATE-SECURE-KEY]

# Database Configuration - Supabase
DATABASE_URL=postgresql://postgres:[SUPABASE-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres

# Redis Configuration - Upstash
REDIS_URL=redis://default:[UPSTASH-PASSWORD]@[REGION].upstash.io:6379

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,https://caresync.vercel.app

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/caresync_backend.log

# Security Configuration
BCRYPT_LOG_ROUNDS=12
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=86400

# Email Configuration - Resend
RESEND_API_KEY=re_[RESEND-API-KEY]
EMAIL_FROM=onboarding@resend.dev
EMAIL_REPLY_TO=support@caresync.com

# File Upload Configuration - Cloudinary
CLOUDINARY_CLOUD_NAME=caresync
CLOUDINARY_API_KEY=[CLOUDINARY-API-KEY]
CLOUDINARY_API_SECRET=[CLOUDINARY-API-SECRET]
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
ALLOWED_EXTENSIONS=jpg,jpeg,png,pdf,doc,docx

# Rate Limiting
RATELIMIT_STORAGE_URL=redis://default:[UPSTASH-PASSWORD]@[REGION].upstash.io:6379
RATELIMIT_DEFAULT=200 per day;50 per hour;10 per minute

# Monitoring and Analytics
SENTRY_DSN=https://[SENTRY-DSN]@[ORG].ingest.sentry.io/[PROJECT]
GOOGLE_ANALYTICS_ID=G-[GA-ID]

# App Configuration
APP_NAME=CareSync
APP_VERSION=1.0.0
APP_ENVIRONMENT=development
```

## 🌐 Frontend Environment Variables

Create `frontend-web/.env` with these values:

```env
# API Configuration
VITE_API_URL=http://localhost:5000/api
VITE_APP_VERSION=1.0.0
VITE_APP_NAME=CareSync

# Analytics
VITE_GOOGLE_ANALYTICS_ID=G-[GA-ID]

# Error Tracking
VITE_SENTRY_DSN=https://[SENTRY-DSN]@[ORG].ingest.sentry.io/[PROJECT]

# Feature Flags
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_ERROR_TRACKING=true
VITE_ENABLE_DEBUG_MODE=false

# App Configuration
VITE_DEFAULT_LANGUAGE=he
VITE_SUPPORTED_LANGUAGES=he,ar,en
VITE_APP_ENVIRONMENT=development
```

## 📋 Service Credentials Checklist

### 1. Supabase (Database)
- [ ] **Project URL**: `https://[PROJECT-REF].supabase.co`
- [ ] **Database Password**: `[SUPABASE-PASSWORD]`
- [ ] **Project Reference**: `[PROJECT-REF]`
- [ ] **API Key**: `[SUPABASE-API-KEY]`

### 2. Upstash (Redis)
- [ ] **Database URL**: `redis://default:[PASSWORD]@[REGION].upstash.io:6379`
- [ ] **Password**: `[UPSTASH-PASSWORD]`
- [ ] **Region**: `[REGION]`

### 3. Resend (Email)
- [ ] **API Key**: `re_[RESEND-API-KEY]`
- [ ] **From Email**: `onboarding@resend.dev`
- [ ] **Reply To**: `support@caresync.com`

### 4. Cloudinary (File Storage)
- [ ] **Cloud Name**: `caresync`
- [ ] **API Key**: `[CLOUDINARY-API-KEY]`
- [ ] **API Secret**: `[CLOUDINARY-API-SECRET]`

### 5. Sentry (Error Tracking)
- [ ] **DSN**: `https://[SENTRY-DSN]@[ORG].ingest.sentry.io/[PROJECT]`
- [ ] **Organization**: `[ORG]`
- [ ] **Project**: `[PROJECT]`

### 6. Google Analytics
- [ ] **Measurement ID**: `G-[GA-ID]`
- [ ] **Property ID**: `[PROPERTY-ID]`

### 7. Vercel (Frontend Hosting)
- [ ] **Project URL**: `https://caresync.vercel.app`
- [ ] **Deployment URL**: `https://[PROJECT].vercel.app`

### 8. Railway (Backend Hosting)
- [ ] **Service URL**: `https://[SERVICE].railway.app`
- [ ] **Deployment URL**: `https://[PROJECT].railway.app`

## 🔑 Generate Secure Keys

Run these commands to generate secure keys:

```bash
# Generate Flask secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate JWT secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate API keys (if needed)
python -c "import secrets; print(secrets.token_hex(32))"
```

## 📝 Service Setup Status

- [ ] **Supabase**: Project created, tables created
- [ ] **Upstash**: Database created, connection tested
- [ ] **SendGrid**: Account created, sender verified
- [ ] **Cloudinary**: Account created, credentials obtained
- [ ] **Sentry**: Project created, DSN obtained
- [ ] **Google Analytics**: Property created, tracking ID obtained
- [ ] **Vercel**: Project deployed, environment variables set
- [ ] **Railway**: Service deployed, environment variables set

## 🔒 Security Notes

1. **Never commit `.env` files** to version control
2. **Rotate keys regularly** (every 90 days)
3. **Use different keys** for development and production
4. **Monitor usage** of all services
5. **Set up alerts** for unusual activity

## 📞 Support Contacts

- **Supabase**: [support@supabase.com](mailto:support@supabase.com)
- **Upstash**: [support@upstash.com](mailto:support@upstash.com)
- **Resend**: [support@resend.com](mailto:support@resend.com)
- **Cloudinary**: [support@cloudinary.com](mailto:support@cloudinary.com)
- **Sentry**: [support@sentry.io](mailto:support@sentry.io)
- **Vercel**: [support@vercel.com](mailto:support@vercel.com)
- **Railway**: [support@railway.app](mailto:support@railway.app)

## 💰 Cost Tracking

**Development (FREE)**:
- Supabase: $0/month
- Upstash: $0/month
- Resend: $0/month
- Cloudinary: $0/month
- Sentry: $0/month
- Vercel: $0/month
- Railway: $0/month

**Production (Recommended)**:
- Supabase Pro: $25/month
- Resend Pro: $20/month
- Railway Pro: $20/month
- Vercel Pro: $20/month
- Sentry Pro: $26/month
- **Total**: ~$111/month

---

**Remember**: Keep this document secure and never share credentials publicly! 