# 🚀 TikTok Analytics + RAG Chatbot - Setup Guide

## 📋 Prerequisites

### 1. **Python Environment**
- Python 3.8+ installed
- pip (Python package manager)
- virtual environment (recommended)

### 2. **Database**
- PostgreSQL 12+ installed and running
- Database user with create privileges

### 3. **API Keys (Required)**
- **OpenAI API Key** (for RAG chatbot) - Get from [OpenAI Platform](https://platform.openai.com/)
- **TikTok API Key** (optional, for real data) - Get from [TikTok for Developers](https://developers.tiktok.com/)

### 4. **System Requirements**
- At least 4GB RAM
- 2GB free disk space
- Internet connection for API calls

## 🛠️ Installation Steps

### Step 1: Clone and Navigate
```bash
cd "C:/Users/Hamza Computers/Tiktok Analytic chatbot/my_tiktok_app"
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
```bash
# Copy environment template
copy env.example .env

# Edit .env file with your API keys
notepad .env
```

### Step 5: Configure .env File
Edit the `.env` file and add your API keys:

```env
# Required: OpenAI API Key (for RAG chatbot)
OPENAI_API_KEY=your_actual_openai_api_key_here

# Optional: Database (uses SQLite by default if not set)
DATABASE_URL=postgresql://user:password@localhost:5432/tiktok_analytics

# Optional: JWT Secret (auto-generated if not set)
JWT_SECRET=your_super_secret_jwt_key_here

# Optional: Other settings
NODE_ENV=development
LOG_LEVEL=INFO
```

### Step 6: Initialize Database (Optional)
If using PostgreSQL:
```bash
# Create database
createdb tiktok_analytics

# Run database migrations (if using Alembic)
alembic upgrade head
```

## 🚀 Running the Application

### Method 1: Using Start Script (Recommended)
```bash
python start.py
```

### Method 2: Direct Uvicorn
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Method 3: Using Docker (Alternative)
```bash
# Build and run with Docker
docker build -t tiktok-analytics .
docker run -p 8000:8000 tiktok-analytics
```

## 🌐 Accessing the Application

Once running, you can access:

- **🏠 Main Application**: http://localhost:8000
- **🤖 AI Chatbot**: http://localhost:8000/chatbot
- **📊 Analytics Dashboard**: http://localhost:8000/explore
- **📚 API Documentation**: http://localhost:8000/docs
- **🏥 Health Check**: http://localhost:8000/health

## 📱 Available Pages

### Core Pages
- **Home**: http://localhost:8000/ - Main landing page
- **Explore**: http://localhost:8000/explore - Analytics overview
- **Products**: http://localhost:8000/products - Product listings
- **Shops**: http://localhost:8000/shops - Shop listings
- **Creators**: http://localhost:8000/creators - Creator listings
- **Categories**: http://localhost:8000/categories - Category listings

### Detail Pages
- **Product Detail**: http://localhost:8000/product/1
- **Shop Detail**: http://localhost:8000/shop/1
- **Creator Detail**: http://localhost:8000/creator/1
- **Category Detail**: http://localhost:8000/category/1

### User Pages
- **Login**: http://localhost:8000/login
- **Signup**: http://localhost:8000/signup
- **Profile**: http://localhost:8000/profile
- **Pricing**: http://localhost:8000/pricing
- **Contact**: http://localhost:8000/contact

## 🤖 Testing the RAG Chatbot

1. Go to http://localhost:8000/chatbot
2. Try these example questions:
   - "How do I set up a TikTok Shop?"
   - "What are the best practices for product optimization?"
   - "How can I increase my shop sales?"
   - "What marketing strategies work best on TikTok?"

## 🔧 Troubleshooting

### Common Issues

#### 1. **Port Already in Use**
```bash
# Kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

#### 2. **Module Not Found Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 3. **OpenAI API Key Issues**
- Verify your API key is correct
- Check your OpenAI account has credits
- Ensure the key has proper permissions

#### 4. **Database Connection Issues**
- Verify PostgreSQL is running
- Check database credentials in .env
- Try using SQLite for testing (remove DATABASE_URL from .env)

### Debug Mode
```bash
# Run with debug logging
uvicorn app.main:app --reload --log-level debug
```

## 📊 Features Available

### ✅ Working Features
- **Complete UI**: All Kalodata-inspired pages
- **RAG Chatbot**: AI-powered TikTok Shop assistance
- **Dummy Data**: Sample products, shops, creators
- **Authentication**: Login/signup system
- **Responsive Design**: Mobile-friendly interface
- **Image Support**: Multiple images per product/shop/creator

### 🔄 In Development
- Real TikTok API integration
- Advanced analytics
- Payment processing
- Email notifications

## 🗄️ Database Schema

The application includes tables for:
- Users and authentication
- Products with multiple images
- Shops with logos and banners
- Creators with profile images
- Videos and thumbnails
- Analytics data
- RAG chatbot conversations
- Knowledge base

## 🔐 Security Notes

- Never commit your `.env` file to version control
- Use strong JWT secrets in production
- Regularly update dependencies
- Monitor API usage and costs

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Check the console logs for error messages
4. Ensure your API keys are valid and have sufficient credits

## 🎯 Next Steps

After successful setup:
1. Test all pages and features
2. Customize the dummy data
3. Integrate real TikTok API data
4. Deploy to production environment
5. Set up monitoring and logging

---

**🎉 Congratulations! Your TikTok Analytics + RAG Chatbot is now running!** 