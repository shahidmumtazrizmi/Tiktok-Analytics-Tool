from fastapi import APIRouter, Query, HTTPException, Depends, Request
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import random
import json
import requests
import logging
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Jinja2 template setup (if not already present)
templates = Jinja2Templates(directory="app/templates")

# Dummy data generators
def generate_dummy_products(count: int = 100):
    """Generate dummy product data"""
    categories = ["Electronics", "Fashion", "Beauty", "Home & Garden", "Sports", "Toys", "Books", "Food", "Health", "Automotive"]
    countries = ["US", "UK", "DE", "FR", "IT", "ES", "CA", "AU", "JP", "KR"]
    
    products = []
    for i in range(count):
        product = {
            "id": f"prod_{i+1:06d}",
            "name": f"Amazing Product {i+1}",
            "shop_name": f"Shop {random.randint(1, 50)}",
            "shop_id": f"shop_{random.randint(1, 50):03d}",
            "price": round(random.uniform(10, 500), 2),
            "currency": "USD",
            "category": random.choice(categories),
            "subcategory": f"Subcategory {random.randint(1, 5)}",
            "country": random.choice(countries),
            "sales_count": random.randint(100, 50000),
            "views": random.randint(1000, 1000000),
            "likes": random.randint(50, 50000),
            "shares": random.randint(10, 5000),
            "comments": random.randint(5, 2000),
            "conversion_rate": round(random.uniform(0.01, 0.15), 4),
            "trend_score": round(random.uniform(50, 100), 2),
            "image_url": f"https://picsum.photos/300/300?random={i}",
            "created_at": datetime.now() - timedelta(days=random.randint(1, 365))
        }
        products.append(product)
    return products

def generate_dummy_shops(count: int = 50):
    """Generate dummy shop data"""
    countries = ["US", "UK", "DE", "FR", "IT", "ES", "CA", "AU", "JP", "KR"]
    
    shops = []
    for i in range(count):
        shop = {
            "id": f"shop_{i+1:03d}",
            "name": f"Amazing Shop {i+1}",
            "owner_name": f"Owner {i+1}",
            "country": random.choice(countries),
            "category": random.choice(["Electronics", "Fashion", "Beauty", "Home", "Sports"]),
            "follower_count": random.randint(1000, 1000000),
            "product_count": random.randint(10, 500),
            "total_orders": random.randint(1000, 100000),
            "total_revenue": round(random.uniform(10000, 1000000), 2),
            "avg_order_value": round(random.uniform(20, 200), 2),
            "conversion_rate": round(random.uniform(0.02, 0.20), 4),
            "is_verified": random.choice([True, False]),
            "rating": round(random.uniform(3.5, 5.0), 1),
            "created_at": datetime.now() - timedelta(days=random.randint(30, 1000))
        }
        shops.append(shop)
    return shops

def generate_dummy_creators(count: int = 100):
    """Generate dummy creator data"""
    categories = ["Lifestyle", "Tech", "Fashion", "Beauty", "Food", "Travel", "Fitness", "Education", "Entertainment", "Business"]
    countries = ["US", "UK", "DE", "FR", "IT", "ES", "CA", "AU", "JP", "KR"]
    
    creators = []
    for i in range(count):
        creator = {
            "id": f"creator_{i+1:06d}",
            "username": f"creator{i+1}",
            "display_name": f"Creator {i+1}",
            "country": random.choice(countries),
            "category": random.choice(categories),
            "follower_count": random.randint(10000, 5000000),
            "following_count": random.randint(100, 10000),
            "video_count": random.randint(50, 2000),
            "like_count": random.randint(100000, 10000000),
            "avg_views": random.randint(10000, 1000000),
            "avg_likes": random.randint(1000, 100000),
            "avg_shares": random.randint(100, 10000),
            "engagement_rate": round(random.uniform(0.02, 0.15), 4),
            "is_verified": random.choice([True, False]),
            "collaboration_price": round(random.uniform(100, 10000), 2),
            "created_at": datetime.now() - timedelta(days=random.randint(100, 2000))
        }
        creators.append(creator)
    return creators

def generate_dummy_categories():
    """Generate dummy category data"""
    categories = [
        {
            "id": "electronics",
            "name": "Electronics",
            "description": "Electronic devices and gadgets",
            "product_count": random.randint(1000, 10000),
            "avg_price": round(random.uniform(50, 300), 2),
            "trending_score": round(random.uniform(70, 95), 2),
            "growth_rate": round(random.uniform(0.05, 0.30), 4),
            "image_url": "https://picsum.photos/400/300?random=1"
        },
        {
            "id": "fashion",
            "name": "Fashion",
            "description": "Clothing, accessories, and fashion items",
            "product_count": random.randint(2000, 15000),
            "avg_price": round(random.uniform(30, 200), 2),
            "trending_score": round(random.uniform(75, 98), 2),
            "growth_rate": round(random.uniform(0.08, 0.35), 4),
            "image_url": "https://picsum.photos/400/300?random=2"
        },
        {
            "id": "beauty",
            "name": "Beauty",
            "description": "Cosmetics, skincare, and beauty products",
            "product_count": random.randint(800, 8000),
            "avg_price": round(random.uniform(20, 150), 2),
            "trending_score": round(random.uniform(80, 96), 2),
            "growth_rate": round(random.uniform(0.10, 0.40), 4),
            "image_url": "https://picsum.photos/400/300?random=3"
        },
        {
            "id": "home-garden",
            "name": "Home & Garden",
            "description": "Home decor, furniture, and garden items",
            "product_count": random.randint(600, 6000),
            "avg_price": round(random.uniform(40, 400), 2),
            "trending_score": round(random.uniform(65, 90), 2),
            "growth_rate": round(random.uniform(0.06, 0.25), 4),
            "image_url": "https://picsum.photos/400/300?random=4"
        },
        {
            "id": "sports",
            "name": "Sports & Outdoors",
            "description": "Sports equipment and outdoor gear",
            "product_count": random.randint(400, 4000),
            "avg_price": round(random.uniform(50, 300), 2),
            "trending_score": round(random.uniform(70, 92), 2),
            "growth_rate": round(random.uniform(0.07, 0.28), 4),
            "image_url": "https://picsum.photos/400/300?random=5"
        }
    ]
    return categories

# Generate dummy data
DUMMY_PRODUCTS = generate_dummy_products(500)
DUMMY_SHOPS = generate_dummy_shops(100)
DUMMY_CREATORS = generate_dummy_creators(200)
DUMMY_CATEGORIES = generate_dummy_categories()

# Fallback dummy data for reviews
DUMMY_REVIEWS = [
    {
        "reviewId": "dummy123",
        "userName": "Test User",
        "rating": 4,
        "comment": "Looks great!",
        "images": [],
        "timestamp": "2025-06-27T12:00:00"
    },
    {
        "reviewId": "dummy124",
        "userName": "Another User",
        "rating": 5,
        "comment": "Fast delivery!",
        "images": [],
        "timestamp": "2025-06-26T14:00:00"
    }
]

def get_product_reviews(product_id: str, region: str = "TH", count: int = 10, cursor: int = 0, sort_type: int = 2):
    """
    Fetch product reviews from TikTok Shop API via RapidAPI.
    Falls back to DUMMY_REVIEWS on error.
    Args:
        product_id (str): TikTok product ID.
        region (str): Region code (default: "TH").
        count (int): Number of reviews to fetch.
        cursor (int): Pagination cursor.
        sort_type (int): Sort type (default: 2).
    Returns:
        list: List of review dicts.
    """
    url = "https://tiktok-shop-api.p.rapidapi.com/api/shop/product/reviews"
    querystring = {
        "productId": product_id,
        "region": region,
        "count": str(count),
        "cursor": str(cursor),
        "sortType": str(sort_type)
    }
    headers = {
        "x-rapidapi-key": "45cc26173amshe51d82ecf68ea77p162486jsnc02a83530a0a",
        "x-rapidapi-host": "tiktok-shop-api.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        data = response.json()
        reviews = data.get("data", {}).get("reviews", DUMMY_REVIEWS)
        if not isinstance(reviews, list) or not reviews:
            reviews = DUMMY_REVIEWS
    except Exception as e:
        logging.warning(f"RapidAPI error: {e}")
        reviews = DUMMY_REVIEWS
    return reviews

@router.get("/trending-products")
async def get_trending_products(
    country: Optional[str] = Query(None, description="Filter by country"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(20, ge=1, le=100, description="Number of products to return"),
    page: int = Query(1, ge=1, description="Page number"),
    search: Optional[str] = Query(None, description="Search term"),
    sort_by: str = Query("trend_score", description="Sort by field"),
    sort_order: str = Query("desc", description="Sort order (asc/desc)")
):
    """Get trending products with filters, search, and pagination"""
    
    # Filter products
    filtered_products = DUMMY_PRODUCTS.copy()
    
    if country:
        filtered_products = [p for p in filtered_products if p["country"] == country.upper()]
    
    if category:
        filtered_products = [p for p in filtered_products if p["category"].lower() == category.lower()]
    
    if search:
        search_lower = search.lower()
        filtered_products = [
            p for p in filtered_products 
            if search_lower in p["name"].lower() or search_lower in p["shop_name"].lower()
        ]
    
    # Sort products
    reverse = sort_order.lower() == "desc"
    filtered_products.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)
    
    # Pagination
    total_count = len(filtered_products)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_products = filtered_products[start_idx:end_idx]
    
    return {
        "success": True,
        "data": paginated_products,
        "meta": {
            "total_count": total_count,
            "page": page,
            "limit": limit,
            "total_pages": (total_count + limit - 1) // limit,
            "has_next": end_idx < total_count,
            "has_prev": page > 1
        }
    }

@router.get("/shops")
async def get_shops(
    country: Optional[str] = Query(None, description="Filter by country"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(20, ge=1, le=100, description="Number of shops to return"),
    page: int = Query(1, ge=1, description="Page number"),
    search: Optional[str] = Query(None, description="Search term"),
    sort_by: str = Query("total_revenue", description="Sort by field"),
    sort_order: str = Query("desc", description="Sort order (asc/desc)")
):
    """Get shops with filters, search, and pagination"""
    
    # Filter shops
    filtered_shops = DUMMY_SHOPS.copy()
    
    if country:
        filtered_shops = [s for s in filtered_shops if s["country"] == country.upper()]
    
    if category:
        filtered_shops = [s for s in filtered_shops if s["category"].lower() == category.lower()]
    
    if search:
        search_lower = search.lower()
        filtered_shops = [
            s for s in filtered_shops 
            if search_lower in s["name"].lower() or search_lower in s["owner_name"].lower()
        ]
    
    # Sort shops
    reverse = sort_order.lower() == "desc"
    filtered_shops.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)
    
    # Pagination
    total_count = len(filtered_shops)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_shops = filtered_shops[start_idx:end_idx]
    
    return {
        "success": True,
        "data": paginated_shops,
        "meta": {
            "total_count": total_count,
            "page": page,
            "limit": limit,
            "total_pages": (total_count + limit - 1) // limit,
            "has_next": end_idx < total_count,
            "has_prev": page > 1
        }
    }

@router.get("/creators")
async def get_creators(
    country: Optional[str] = Query(None, description="Filter by country"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(20, ge=1, le=100, description="Number of creators to return"),
    page: int = Query(1, ge=1, description="Page number"),
    search: Optional[str] = Query(None, description="Search term"),
    sort_by: str = Query("follower_count", description="Sort by field"),
    sort_order: str = Query("desc", description="Sort order (asc/desc)")
):
    """Get creators with filters, search, and pagination"""
    
    # Filter creators
    filtered_creators = DUMMY_CREATORS.copy()
    
    if country:
        filtered_creators = [c for c in filtered_creators if c["country"] == country.upper()]
    
    if category:
        filtered_creators = [c for c in filtered_creators if c["category"].lower() == category.lower()]
    
    if search:
        search_lower = search.lower()
        filtered_creators = [
            c for c in filtered_creators 
            if search_lower in c["username"].lower() or search_lower in c["display_name"].lower()
        ]
    
    # Sort creators
    reverse = sort_order.lower() == "desc"
    filtered_creators.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)
    
    # Pagination
    total_count = len(filtered_creators)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_creators = filtered_creators[start_idx:end_idx]
    
    return {
        "success": True,
        "data": paginated_creators,
        "meta": {
            "total_count": total_count,
            "page": page,
            "limit": limit,
            "total_pages": (total_count + limit - 1) // limit,
            "has_next": end_idx < total_count,
            "has_prev": page > 1
        }
    }

@router.get("/categories")
async def get_categories():
    """Get all categories"""
    return {
        "success": True,
        "data": DUMMY_CATEGORIES
    }

@router.get("/product/{product_id}")
async def get_product_details(product_id: str):
    """Get detailed product information"""
    product = next((p for p in DUMMY_PRODUCTS if p["id"] == product_id), None)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Add additional details
    product["detailed_info"] = {
        "description": f"This is a detailed description of {product['name']}. It's an amazing product that customers love!",
        "specifications": {
            "brand": f"Brand {random.randint(1, 10)}",
            "weight": f"{random.randint(100, 2000)}g",
            "dimensions": f"{random.randint(10, 50)}x{random.randint(10, 50)}x{random.randint(5, 20)}cm",
            "material": random.choice(["Plastic", "Metal", "Wood", "Fabric", "Glass"]),
            "warranty": f"{random.randint(1, 3)} years"
        },
        "reviews": {
            "average_rating": round(random.uniform(3.5, 5.0), 1),
            "total_reviews": random.randint(50, 1000),
            "positive_percentage": random.randint(80, 98)
        },
        "related_products": random.sample([p["id"] for p in DUMMY_PRODUCTS if p["id"] != product_id], min(5, len(DUMMY_PRODUCTS)-1))
    }
    
    return {
        "success": True,
        "data": product
    }

@router.get("/shop/{shop_id}")
async def get_shop_details(shop_id: str):
    """Get detailed shop information"""
    shop = next((s for s in DUMMY_SHOPS if s["id"] == shop_id), None)
    
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    # Add shop products
    shop_products = [p for p in DUMMY_PRODUCTS if p["shop_id"] == shop_id][:10]
    
    shop["products"] = shop_products
    shop["analytics"] = {
        "daily_sales": random.randint(50, 500),
        "weekly_growth": round(random.uniform(0.05, 0.30), 4),
        "monthly_revenue": round(random.uniform(5000, 50000), 2),
        "customer_satisfaction": round(random.uniform(4.0, 5.0), 1)
    }
    
    return {
        "success": True,
        "data": shop
    }

@router.get("/creator/{creator_id}")
async def get_creator_details(creator_id: str):
    """Get detailed creator information"""
    creator = next((c for c in DUMMY_CREATORS if c["id"] == creator_id), None)
    
    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")
    
    # Add creator videos
    creator["videos"] = [
        {
            "id": f"video_{i}",
            "title": f"Amazing Video {i}",
            "views": random.randint(10000, 1000000),
            "likes": random.randint(1000, 100000),
            "shares": random.randint(100, 10000),
            "created_at": datetime.now() - timedelta(days=random.randint(1, 365))
        }
        for i in range(1, 11)
    ]
    
    creator["collaboration_info"] = {
        "availability": random.choice(["Available", "Limited", "Unavailable"]),
        "response_rate": random.randint(70, 100),
        "avg_response_time": f"{random.randint(1, 48)} hours",
        "preferred_categories": random.sample(["Electronics", "Fashion", "Beauty", "Home", "Sports"], 3)
    }
    
    return {
        "success": True,
        "data": creator
    }

@router.get("/category/{category_id}")
async def get_category_details(category_id: str):
    """Get detailed category information"""
    category = next((c for c in DUMMY_CATEGORIES if c["id"] == category_id), None)
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Add category products
    category_products = [p for p in DUMMY_PRODUCTS if p["category"].lower() == category["name"].lower()][:20]
    
    category["products"] = category_products
    category["market_insights"] = {
        "total_market_size": f"${random.randint(1000000, 10000000):,}",
        "growth_rate": round(random.uniform(0.05, 0.40), 4),
        "competition_level": random.choice(["Low", "Medium", "High"]),
        "seasonality": random.choice(["Year-round", "Seasonal", "Trend-based"]),
        "top_brands": [f"Brand {i}" for i in range(1, 6)]
    }
    
    return {
        "success": True,
        "data": category
    }

@router.get("/stats/overview")
async def get_overview_stats():
    """Get overview statistics"""
    return {
        "success": True,
        "data": {
            "total_products": len(DUMMY_PRODUCTS),
            "total_shops": len(DUMMY_SHOPS),
            "total_creators": len(DUMMY_CREATORS),
            "total_categories": len(DUMMY_CATEGORIES),
            "total_sales": sum(p["sales_count"] for p in DUMMY_PRODUCTS),
            "total_revenue": sum(s["total_revenue"] for s in DUMMY_SHOPS),
            "avg_product_price": round(sum(p["price"] for p in DUMMY_PRODUCTS) / len(DUMMY_PRODUCTS), 2),
            "top_countries": ["US", "UK", "DE", "FR", "IT"],
            "trending_categories": ["Fashion", "Beauty", "Electronics", "Home & Garden", "Sports"]
        }
    }

@router.get("/product/{product_id}/reviews")
async def product_reviews(request: Request, product_id: str):
    reviews = get_product_reviews(product_id)
    return templates.TemplateResponse(
        "category_details.html",
        {
            "request": request,
            "product_id": product_id,
            "reviews": reviews,
        }
    ) 