from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
from contextlib import asynccontextmanager
import logging

from app.routers import analytics, rag_chat, auth
from app.core.config import settings
from app.core.database import init_db
from app.rag.vector_db import vector_db
from app.rag.embeddings import embedding_manager
from app.rag.scraper import tiktok_scraper

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting TikTok Analytics + RAG Chatbot API...")
    await init_db()
    
    # Initialize RAG components
    logger.info("Initializing RAG components...")
    try:
        # Initialize vector database
        vector_db._initialize_client()
        logger.info("Vector database initialized successfully")
        
        # Initialize embeddings
        logger.info("Embeddings manager initialized successfully")
        
        # Initialize scraper
        logger.info("TikTok scraper initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing RAG components: {e}")
    
    logger.info("Database and RAG components initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down TikTok Analytics + RAG Chatbot API...")

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title="TikTok Analytics + RAG Chatbot",
        description="Comprehensive TikTok Shop analytics with AI-powered chatbot",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # Security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure for production
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Mount static files
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    
    # Templates
    templates = Jinja2Templates(directory="app/templates")
    
    # Include routers
    app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
    app.include_router(rag_chat.router, prefix="/api/chat", tags=["chat"])
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    
    # Dummy data functions
    def get_dummy_products():
        return [
            {"id": "1", "name": "Wireless Earbuds Pro", "category": "Electronics", "price": "89.99", "sales": "1,234", "views": "45K", "rating": "4.8"},
            {"id": "2", "name": "Smart Watch Series 5", "category": "Electronics", "price": "199.99", "sales": "856", "views": "32K", "rating": "4.6"},
            {"id": "3", "name": "Bluetooth Speaker", "category": "Electronics", "price": "59.99", "sales": "2,145", "views": "78K", "rating": "4.7"},
            {"id": "4", "name": "Phone Case Premium", "category": "Accessories", "price": "24.99", "sales": "3,456", "views": "120K", "rating": "4.9"},
            {"id": "5", "name": "Wireless Charger", "category": "Electronics", "price": "39.99", "sales": "1,789", "views": "56K", "rating": "4.5"},
            {"id": "6", "name": "Gaming Headset", "category": "Electronics", "price": "129.99", "sales": "567", "views": "23K", "rating": "4.4"}
        ]
    
    def get_dummy_shops():
        return [
            {"id": "1", "name": "TechGadget Store", "category": "Electronics", "products": "156", "sales": "12,345", "rating": "4.8", "followers": "45K"},
            {"id": "2", "name": "Fashion Forward", "category": "Fashion", "products": "89", "sales": "8,901", "rating": "4.6", "followers": "32K"},
            {"id": "3", "name": "Beauty Essentials", "category": "Beauty", "products": "234", "sales": "15,678", "rating": "4.7", "followers": "67K"},
            {"id": "4", "name": "Home & Garden Pro", "category": "Home", "products": "123", "sales": "6,789", "rating": "4.5", "followers": "28K"},
            {"id": "5", "name": "Sports Gear Hub", "category": "Sports", "products": "78", "sales": "4,567", "rating": "4.4", "followers": "19K"},
            {"id": "6", "name": "Kids Toys World", "category": "Toys", "products": "345", "sales": "9,876", "rating": "4.9", "followers": "52K"}
        ]
    
    def get_dummy_creators():
        return [
            {"id": "1", "name": "TechReviewer", "category": "Technology", "followers": "2.1M", "videos": "156", "engagement": "8.5", "likes": "45M"},
            {"id": "2", "name": "Fashionista", "category": "Fashion", "followers": "1.8M", "videos": "234", "engagement": "7.2", "likes": "38M"},
            {"id": "3", "name": "BeautyGuru", "category": "Beauty", "followers": "3.2M", "videos": "189", "engagement": "9.1", "likes": "67M"},
            {"id": "4", "name": "LifestylePro", "category": "Lifestyle", "followers": "1.5M", "videos": "267", "engagement": "6.8", "likes": "29M"},
            {"id": "5", "name": "FoodMaster", "category": "Food", "followers": "2.8M", "videos": "145", "engagement": "8.9", "likes": "52M"},
            {"id": "6", "name": "FitnessCoach", "category": "Fitness", "followers": "1.9M", "videos": "198", "engagement": "7.5", "likes": "41M"}
        ]
    
    def get_dummy_categories():
        return [
            {"id": "1", "name": "Electronics", "icon": "📱", "description": "Latest gadgets and tech products", "products": "1,234", "sales": "45,678", "revenue": "2.3M", "growth": "15.2"},
            {"id": "2", "name": "Fashion", "icon": "👗", "description": "Trendy clothing and accessories", "products": "2,345", "sales": "67,890", "revenue": "1.8M", "growth": "12.8"},
            {"id": "3", "name": "Beauty", "icon": "💄", "description": "Cosmetics and skincare products", "products": "1,567", "sales": "34,567", "revenue": "1.2M", "growth": "18.5"},
            {"id": "4", "name": "Home & Garden", "icon": "🏠", "description": "Home improvement and decor", "products": "890", "sales": "23,456", "revenue": "890K", "growth": "9.7"},
            {"id": "5", "name": "Sports", "icon": "⚽", "description": "Sports equipment and gear", "products": "678", "sales": "18,234", "revenue": "567K", "growth": "11.3"},
            {"id": "6", "name": "Toys & Games", "icon": "🎮", "description": "Entertainment for all ages", "products": "1,123", "sales": "29,876", "revenue": "745K", "growth": "14.6"}
        ]
    
    def get_dummy_trending_products():
        return [
            {"id": "1", "name": "Wireless Earbuds Pro", "category": "Electronics", "price": "89.99", "sales": "1,234"},
            {"id": "2", "name": "Smart Watch Series 5", "category": "Electronics", "price": "199.99", "sales": "856"},
            {"id": "3", "name": "Bluetooth Speaker", "category": "Electronics", "price": "59.99", "sales": "2,145"},
            {"id": "4", "name": "Phone Case Premium", "category": "Accessories", "price": "24.99", "sales": "3,456"}
        ]
    
    def get_dummy_top_shops():
        return [
            {"id": "1", "name": "TechGadget Store", "category": "Electronics", "products": "156", "sales": "12,345"},
            {"id": "2", "name": "Fashion Forward", "category": "Fashion", "products": "89", "sales": "8,901"},
            {"id": "3", "name": "Beauty Essentials", "category": "Beauty", "products": "234", "sales": "15,678"}
        ]
    
    def get_dummy_popular_creators():
        return [
            {"id": "1", "name": "TechReviewer", "followers": "2.1M", "videos": "156", "engagement": "8.5"},
            {"id": "2", "name": "Fashionista", "followers": "1.8M", "videos": "234", "engagement": "7.2"},
            {"id": "3", "name": "BeautyGuru", "followers": "3.2M", "videos": "189", "engagement": "9.1"}
        ]
    
    # Root route
    @app.get("/")
    async def root(request: Request):
        return templates.TemplateResponse("home.html", {"request": request})
    
    # Home page
    @app.get("/home")
    async def home(request: Request):
        return templates.TemplateResponse("home.html", {"request": request})
    
    # Explore page
    @app.get("/explore")
    async def explore(request: Request):
        return templates.TemplateResponse("explore.html", {
            "request": request,
            "trending_products": get_dummy_trending_products(),
            "top_shops": get_dummy_top_shops(),
            "popular_creators": get_dummy_popular_creators(),
            "categories": get_dummy_categories()
        })
    
    # Products page
    @app.get("/products")
    async def products(request: Request):
        return templates.TemplateResponse("products.html", {
            "request": request,
            "products": get_dummy_products()
        })
    
    # Product detail page
    @app.get("/product/{product_id}")
    async def product_detail(request: Request, product_id: str):
        # Find product by ID (in real app, this would be from database)
        products = get_dummy_products()
        product = next((p for p in products if p["id"] == product_id), products[0])
        related_products = products[:4]  # First 4 as related
        
        return templates.TemplateResponse("product_detail.html", {
            "request": request,
            "product": product,
            "related_products": related_products
        })
    
    # Shops page
    @app.get("/shops")
    async def shops(request: Request):
        return templates.TemplateResponse("shops.html", {
            "request": request,
            "shops": get_dummy_shops()
        })
    
    # Shop detail page
    @app.get("/shop/{shop_id}")
    async def shop_detail(request: Request, shop_id: str):
        # Find shop by ID (in real app, this would be from database)
        shops = get_dummy_shops()
        shop = next((s for s in shops if s["id"] == shop_id), shops[0])
        shop_products = get_dummy_products()[:4]  # First 4 as shop products
        
        return templates.TemplateResponse("shop_detail.html", {
            "request": request,
            "shop": shop,
            "shop_products": shop_products
        })
    
    # Creators page
    @app.get("/creators")
    async def creators(request: Request):
        return templates.TemplateResponse("creators.html", {
            "request": request,
            "creators": get_dummy_creators()
        })
    
    # Creator detail page
    @app.get("/creator/{creator_id}")
    async def creator_detail(request: Request, creator_id: str):
        # Find creator by ID (in real app, this would be from database)
        creators = get_dummy_creators()
        creator = next((c for c in creators if c["id"] == creator_id), creators[0])
        creator_videos = [
            {"title": "Latest Tech Review", "views": "45K", "likes": "2.3K", "comments": "156"},
            {"title": "Unboxing New Gadget", "views": "32K", "likes": "1.8K", "comments": "89"},
            {"title": "Tech Tips & Tricks", "views": "28K", "likes": "1.5K", "comments": "67"},
            {"title": "Product Comparison", "views": "56K", "likes": "3.2K", "comments": "234"}
        ]
        
        return templates.TemplateResponse("creator_detail.html", {
            "request": request,
            "creator": creator,
            "creator_videos": creator_videos
        })
    
    # Categories page
    @app.get("/categories")
    async def categories(request: Request):
        return templates.TemplateResponse("categories.html", {
            "request": request,
            "categories": get_dummy_categories()
        })
    
    # Category detail page
    @app.get("/category/{category_id}")
    async def category_detail(request: Request, category_id: str):
        # Find category by ID (in real app, this would be from database)
        categories = get_dummy_categories()
        category = next((c for c in categories if c["id"] == category_id), categories[0])
        category_products = get_dummy_products()[:4]  # First 4 as category products
        category_shops = get_dummy_shops()[:3]  # First 3 as category shops
        
        return templates.TemplateResponse("category_detail.html", {
            "request": request,
            "category": category,
            "category_products": category_products,
            "category_shops": category_shops
        })
    
    # Pricing page
    @app.get("/pricing")
    async def pricing(request: Request):
        return templates.TemplateResponse("pricing.html", {"request": request})
    
    # Chatbot page
    @app.get("/chatbot")
    async def chatbot(request: Request):
        return templates.TemplateResponse("chatbot.html", {"request": request})
    
    # Profile page
    @app.get("/profile")
    async def profile(request: Request):
        return templates.TemplateResponse("profile.html", {"request": request})
    
    # Login page
    @app.get("/login")
    async def login(request: Request):
        return templates.TemplateResponse("login.html", {"request": request})
    
    # Signup page
    @app.get("/signup")
    async def signup(request: Request):
        return templates.TemplateResponse("signup.html", {"request": request})
    
    # Reset password page
    @app.get("/reset-password")
    async def reset_password(request: Request):
        return templates.TemplateResponse("reset_password.html", {"request": request})
    
    # Contact page (for enterprise pricing)
    @app.get("/contact")
    async def contact(request: Request):
        return templates.TemplateResponse("contact.html", {"request": request})
    
    # Health check
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "TikTok Analytics + RAG Chatbot"}
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 