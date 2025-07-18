# 🚀 TikTok Analytics + RAG Chatbot

A comprehensive TikTok Shop analytics platform with AI-powered chatbot, inspired by Kalodata.

## 🎯 Features

- **📊 Analytics Dashboard** - Track products, shops, creators, and categories
- **🤖 AI Chatbot** - RAG-powered assistance for TikTok Shop questions
- **🖼️ Multi-Image Support** - Multiple images for products, shops, creators
- **📱 Responsive Design** - Mobile-friendly interface
- **🔐 Authentication** - User login/signup system
- **📈 Real-time Data** - Live analytics and trending information

## 🛠️ Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API Key (for chatbot)

### 1. Install Dependencies
```bash
cd my_tiktok_app
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
copy env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Run the Application
```bash
python start.py
```

### 4. Access the App
- **Main App**: http://localhost:8000
- **Chatbot**: http://localhost:8000/chatbot
- **API Docs**: http://localhost:8000/docs

## 📱 Available Pages

### Core Pages
- **Home**: `/` - Landing page
- **Explore**: `/explore` - Analytics overview
- **Products**: `/products` - Product listings
- **Shops**: `/shops` - Shop listings
- **Creators**: `/creators` - Creator listings
- **Categories**: `/categories` - Category listings

### Detail Pages
- **Product Detail**: `/product/{id}`
- **Shop Detail**: `/shop/{id}`
- **Creator Detail**: `/creator/{id}`
- **Category Detail**: `/category/{id}`

### User Pages
- **Login**: `/login`
- **Signup**: `/signup`
- **Profile**: `/profile`
- **Pricing**: `/pricing`
- **Contact**: `/contact`

## 🤖 Testing the Chatbot

Visit http://localhost:8000/chatbot and try:
- "How do I set up a TikTok Shop?"
- "What are the best practices for product optimization?"
- "How can I increase my shop sales?"

## 🗄️ Database Schema

The app includes tables for:
- Users and authentication
- Products with multiple images
- Shops with logos and banners
- Creators with profile images
- Videos and thumbnails
- Analytics data
- RAG chatbot conversations

## 🔧 Configuration

Edit `.env` file to configure:
- OpenAI API Key (required for chatbot)
- Database connection
- JWT secrets
- Other settings

## 🚀 Deployment

### Development
```bash
python start.py
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker
```bash
docker build -t tiktok-analytics .
docker run -p 8000:8000 tiktok-analytics
```

## 📊 Tech Stack

- **Backend**: FastAPI, Python
- **Frontend**: Jinja2, TailwindCSS
- **Database**: PostgreSQL (optional, SQLite by default)
- **AI**: OpenAI GPT-4, LangChain
- **Vector DB**: ChromaDB
- **Authentication**: JWT

## 🎨 UI Features

- **Responsive Design** - Works on all devices
- **Dark/Light Mode** - Theme switching
- **Image Galleries** - Multiple images per item
- **Real-time Updates** - Live data refresh
- **Interactive Charts** - Analytics visualization

## 🔐 Security

- JWT authentication
- Password hashing
- API key management
- CORS protection

## 📞 Support

For issues or questions:
1. Check the console logs
2. Verify API keys are correct
3. Ensure all dependencies are installed
4. Check the troubleshooting section

## 🎯 Next Steps

- Integrate real TikTok API
- Add payment processing
- Implement email notifications
- Deploy to production

---

**🎉 Ready to analyze TikTok Shop data with AI!** 