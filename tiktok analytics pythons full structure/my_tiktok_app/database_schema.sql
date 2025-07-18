-- TikTok Analytics Platform Database Schema
-- Comprehensive database structure with image handling for all components

-- =====================================================
-- USERS AND AUTHENTICATION
-- =====================================================

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    profile_image_url VARCHAR(500),
    company_name VARCHAR(200),
    phone VARCHAR(20),
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    subscription_tier VARCHAR(20) DEFAULT 'free', -- free, pro, enterprise
    subscription_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- CATEGORIES AND TAGS
-- =====================================================

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(50), -- emoji or icon class
    parent_category_id INTEGER REFERENCES categories(id),
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- SHOPS AND SHOP IMAGES
-- =====================================================

CREATE TABLE shops (
    id SERIAL PRIMARY KEY,
    shop_id VARCHAR(100) UNIQUE NOT NULL, -- TikTok Shop ID
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES categories(id),
    logo_url VARCHAR(500),
    banner_url VARCHAR(500),
    website_url VARCHAR(500),
    location VARCHAR(200),
    country VARCHAR(100),
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    followers_count INTEGER DEFAULT 0,
    products_count INTEGER DEFAULT 0,
    total_sales INTEGER DEFAULT 0,
    total_revenue DECIMAL(15,2) DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE shop_images (
    id SERIAL PRIMARY KEY,
    shop_id INTEGER REFERENCES shops(id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    image_type VARCHAR(50) NOT NULL, -- logo, banner, gallery, featured
    alt_text VARCHAR(200),
    sort_order INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE shop_analytics (
    id SERIAL PRIMARY KEY,
    shop_id INTEGER REFERENCES shops(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    views INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    sales INTEGER DEFAULT 0,
    revenue DECIMAL(15,2) DEFAULT 0,
    conversion_rate DECIMAL(5,4) DEFAULT 0,
    avg_order_value DECIMAL(10,2) DEFAULT 0,
    customer_acquisition_cost DECIMAL(10,2) DEFAULT 0,
    return_on_ad_spend DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(shop_id, date)
);

-- =====================================================
-- PRODUCTS AND PRODUCT IMAGES
-- =====================================================

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(100) UNIQUE NOT NULL, -- TikTok Product ID
    shop_id INTEGER REFERENCES shops(id) ON DELETE CASCADE,
    name VARCHAR(300) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES categories(id),
    price DECIMAL(10,2) NOT NULL,
    original_price DECIMAL(10,2),
    currency VARCHAR(3) DEFAULT 'USD',
    sku VARCHAR(100),
    brand VARCHAR(100),
    model VARCHAR(100),
    weight DECIMAL(8,2),
    dimensions VARCHAR(100),
    color VARCHAR(50),
    size VARCHAR(50),
    material VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    is_trending BOOLEAN DEFAULT FALSE,
    stock_quantity INTEGER DEFAULT 0,
    sold_quantity INTEGER DEFAULT 0,
    views_count INTEGER DEFAULT 0,
    likes_count INTEGER DEFAULT 0,
    shares_count INTEGER DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE product_images (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    image_type VARCHAR(50) NOT NULL, -- main, gallery, detail, thumbnail
    alt_text VARCHAR(200),
    sort_order INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE,
    width INTEGER,
    height INTEGER,
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE product_variants (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    variant_name VARCHAR(100) NOT NULL,
    variant_value VARCHAR(100) NOT NULL,
    price_adjustment DECIMAL(10,2) DEFAULT 0,
    stock_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE product_analytics (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    views INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    sales INTEGER DEFAULT 0,
    revenue DECIMAL(15,2) DEFAULT 0,
    conversion_rate DECIMAL(5,4) DEFAULT 0,
    avg_order_value DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, date)
);

-- =====================================================
-- CREATORS AND CREATOR IMAGES
-- =====================================================

CREATE TABLE creators (
    id SERIAL PRIMARY KEY,
    creator_id VARCHAR(100) UNIQUE NOT NULL, -- TikTok Creator ID
    username VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(200),
    bio TEXT,
    profile_image_url VARCHAR(500),
    banner_image_url VARCHAR(500),
    category_id INTEGER REFERENCES categories(id),
    location VARCHAR(200),
    country VARCHAR(100),
    language VARCHAR(50),
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    followers_count INTEGER DEFAULT 0,
    following_count INTEGER DEFAULT 0,
    videos_count INTEGER DEFAULT 0,
    likes_count INTEGER DEFAULT 0,
    total_views BIGINT DEFAULT 0,
    engagement_rate DECIMAL(5,4) DEFAULT 0,
    avg_views_per_video INTEGER DEFAULT 0,
    avg_likes_per_video INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE creator_images (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES creators(id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    image_type VARCHAR(50) NOT NULL, -- profile, banner, gallery, featured
    alt_text VARCHAR(200),
    sort_order INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE creator_analytics (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES creators(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    followers_gained INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,4) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(creator_id, date)
);

-- =====================================================
-- VIDEOS AND VIDEO IMAGES
-- =====================================================

CREATE TABLE videos (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(100) UNIQUE NOT NULL, -- TikTok Video ID
    creator_id INTEGER REFERENCES creators(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    title VARCHAR(300),
    description TEXT,
    thumbnail_url VARCHAR(500),
    video_url VARCHAR(500),
    duration INTEGER, -- in seconds
    category_id INTEGER REFERENCES categories(id),
    tags TEXT[], -- array of tags
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    is_trending BOOLEAN DEFAULT FALSE,
    views_count INTEGER DEFAULT 0,
    likes_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    shares_count INTEGER DEFAULT 0,
    saves_count INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,4) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP
);

CREATE TABLE video_images (
    id SERIAL PRIMARY KEY,
    video_id INTEGER REFERENCES videos(id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    image_type VARCHAR(50) NOT NULL, -- thumbnail, screenshot, gallery
    alt_text VARCHAR(200),
    sort_order INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE video_analytics (
    id SERIAL PRIMARY KEY,
    video_id INTEGER REFERENCES videos(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    saves INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,4) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(video_id, date)
);

-- =====================================================
-- LIVESTREAMS
-- =====================================================

CREATE TABLE livestreams (
    id SERIAL PRIMARY KEY,
    livestream_id VARCHAR(100) UNIQUE NOT NULL,
    creator_id INTEGER REFERENCES creators(id) ON DELETE CASCADE,
    title VARCHAR(300),
    description TEXT,
    thumbnail_url VARCHAR(500),
    stream_url VARCHAR(500),
    status VARCHAR(20) DEFAULT 'scheduled', -- scheduled, live, ended
    scheduled_start TIMESTAMP,
    actual_start TIMESTAMP,
    ended_at TIMESTAMP,
    duration INTEGER, -- in seconds
    peak_viewers INTEGER DEFAULT 0,
    total_viewers INTEGER DEFAULT 0,
    likes_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    shares_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- RANKINGS AND TRENDING
-- =====================================================

CREATE TABLE product_rankings (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id),
    ranking_type VARCHAR(50) NOT NULL, -- trending, best_seller, most_viewed, highest_rated
    rank_position INTEGER NOT NULL,
    score DECIMAL(10,4) DEFAULT 0,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, ranking_type, date)
);

CREATE TABLE shop_rankings (
    id SERIAL PRIMARY KEY,
    shop_id INTEGER REFERENCES shops(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id),
    ranking_type VARCHAR(50) NOT NULL, -- top_seller, most_followed, highest_rated
    rank_position INTEGER NOT NULL,
    score DECIMAL(10,4) DEFAULT 0,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(shop_id, ranking_type, date)
);

CREATE TABLE creator_rankings (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES creators(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id),
    ranking_type VARCHAR(50) NOT NULL, -- most_followed, highest_engagement, most_viral
    rank_position INTEGER NOT NULL,
    score DECIMAL(10,4) DEFAULT 0,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(creator_id, ranking_type, date)
);

-- =====================================================
-- RAG CHATBOT SYSTEM
-- =====================================================

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    conversation_id VARCHAR(100) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE conversation_messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- user, assistant, system
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE knowledge_base (
    id SERIAL PRIMARY KEY,
    title VARCHAR(300) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(100),
    tags TEXT[],
    source_url VARCHAR(500),
    embedding_id VARCHAR(100), -- reference to vector database
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- USER PREFERENCES AND SETTINGS
-- =====================================================

CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    preference_key VARCHAR(100) NOT NULL,
    preference_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, preference_key)
);

CREATE TABLE user_favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    item_type VARCHAR(50) NOT NULL, -- product, shop, creator, category
    item_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, item_type, item_id)
);

-- =====================================================
-- NOTIFICATIONS AND ALERTS
-- =====================================================

CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50) NOT NULL, -- alert, update, reminder
    is_read BOOLEAN DEFAULT FALSE,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- SEARCH AND FILTERS
-- =====================================================

CREATE TABLE search_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    query TEXT NOT NULL,
    filters JSONB,
    results_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_subscription_tier ON users(subscription_tier);

-- Shops
CREATE INDEX idx_shops_category_id ON shops(category_id);
CREATE INDEX idx_shops_is_active ON shops(is_active);
CREATE INDEX idx_shops_followers_count ON shops(followers_count);
CREATE INDEX idx_shops_total_sales ON shops(total_sales);

-- Products
CREATE INDEX idx_products_shop_id ON products(shop_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_is_trending ON products(is_trending);
CREATE INDEX idx_products_views_count ON products(views_count);

-- Creators
CREATE INDEX idx_creators_category_id ON creators(category_id);
CREATE INDEX idx_creators_followers_count ON creators(followers_count);
CREATE INDEX idx_creators_engagement_rate ON creators(engagement_rate);

-- Videos
CREATE INDEX idx_videos_creator_id ON videos(creator_id);
CREATE INDEX idx_videos_product_id ON videos(product_id);
CREATE INDEX idx_videos_views_count ON videos(views_count);
CREATE INDEX idx_videos_created_at ON videos(created_at);

-- Analytics
CREATE INDEX idx_shop_analytics_shop_date ON shop_analytics(shop_id, date);
CREATE INDEX idx_product_analytics_product_date ON product_analytics(product_id, date);
CREATE INDEX idx_creator_analytics_creator_date ON creator_analytics(creator_id, date);

-- Rankings
CREATE INDEX idx_product_rankings_type_date ON product_rankings(ranking_type, date);
CREATE INDEX idx_shop_rankings_type_date ON shop_rankings(ranking_type, date);
CREATE INDEX idx_creator_rankings_type_date ON creator_rankings(ranking_type, date);

-- Chat
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversation_messages_conversation_id ON conversation_messages(conversation_id);

-- =====================================================
-- SAMPLE DATA INSERTS
-- =====================================================

-- Insert sample categories
INSERT INTO categories (name, slug, description, icon) VALUES
('Electronics', 'electronics', 'Latest gadgets and tech products', '📱'),
('Fashion', 'fashion', 'Trendy clothing and accessories', '👗'),
('Beauty', 'beauty', 'Cosmetics and skincare products', '💄'),
('Home & Garden', 'home-garden', 'Home improvement and decor', '🏠'),
('Sports', 'sports', 'Sports equipment and gear', '⚽'),
('Toys & Games', 'toys-games', 'Entertainment for all ages', '🎮');

-- Insert sample shops
INSERT INTO shops (shop_id, name, description, category_id, logo_url, followers_count, products_count, total_sales, rating) VALUES
('shop_001', 'TechGadget Store', 'Leading electronics store on TikTok Shop', 1, 'https://example.com/logos/techgadget.png', 45000, 156, 12345, 4.8),
('shop_002', 'Fashion Forward', 'Trendy fashion for everyone', 2, 'https://example.com/logos/fashionforward.png', 32000, 89, 8901, 4.6),
('shop_003', 'Beauty Essentials', 'Premium beauty products', 3, 'https://example.com/logos/beautyessentials.png', 67000, 234, 15678, 4.7);

-- Insert sample products
INSERT INTO products (product_id, shop_id, name, description, category_id, price, views_count, sold_quantity, rating) VALUES
('prod_001', 1, 'Wireless Earbuds Pro', 'High-quality wireless earbuds with noise cancellation', 1, 89.99, 45000, 1234, 4.8),
('prod_002', 1, 'Smart Watch Series 5', 'Advanced smartwatch with health tracking features', 1, 199.99, 32000, 856, 4.6),
('prod_003', 2, 'Bluetooth Speaker', 'Portable bluetooth speaker with amazing sound quality', 1, 59.99, 78000, 2145, 4.7);

-- Insert sample creators
INSERT INTO creators (creator_id, username, display_name, bio, category_id, followers_count, videos_count, engagement_rate) VALUES
('creator_001', 'techreviewer', 'TechReviewer', 'Tech reviewer and influencer', 1, 2100000, 156, 8.5),
('creator_002', 'fashionista', 'Fashionista', 'Fashion and lifestyle content creator', 2, 1800000, 234, 7.2),
('creator_003', 'beautyguru', 'BeautyGuru', 'Beauty and makeup expert', 3, 3200000, 189, 9.1);

-- Insert sample product images
INSERT INTO product_images (product_id, image_url, image_type, is_primary)
VALUES
  (1, 'https://img1.jpg', 'main', TRUE),
  (1, 'https://img2.jpg', 'gallery', FALSE),
  (1, 'https://img3.jpg', 'gallery', FALSE);

-- Insert sample shop images
INSERT INTO shop_images (shop_id, image_url, image_type, alt_text, is_primary) VALUES
(1, 'https://example.com/shops/techgadget_logo.png', 'logo', 'TechGadget Store Logo', TRUE),
(1, 'https://example.com/shops/techgadget_banner.jpg', 'banner', 'TechGadget Store Banner', FALSE),
(2, 'https://example.com/shops/fashionforward_logo.png', 'logo', 'Fashion Forward Logo', TRUE),
(2, 'https://example.com/shops/fashionforward_banner.jpg', 'banner', 'Fashion Forward Banner', FALSE);

-- Insert sample creator images
INSERT INTO creator_images (creator_id, image_url, image_type, alt_text, is_primary) VALUES
(1, 'https://example.com/creators/techreviewer_profile.jpg', 'profile', 'TechReviewer Profile Picture', TRUE),
(1, 'https://example.com/creators/techreviewer_banner.jpg', 'banner', 'TechReviewer Banner', FALSE),
(2, 'https://example.com/creators/fashionista_profile.jpg', 'profile', 'Fashionista Profile Picture', TRUE),
(2, 'https://example.com/creators/fashionista_banner.jpg', 'banner', 'Fashionista Banner', FALSE);

-- Insert sample knowledge base
INSERT INTO knowledge_base (title, content, category, tags) VALUES
('TikTok Shop Setup Guide', 'Complete guide to setting up your TikTok Shop account, including verification process and requirements.', 'setup', ARRAY['setup', 'verification', 'account']),
('Product Optimization Tips', 'Best practices for optimizing your TikTok Shop product listings to increase sales and visibility.', 'optimization', ARRAY['optimization', 'product', 'sales']),
('Marketing Strategies', 'Effective marketing strategies for promoting your TikTok Shop products and growing your business.', 'marketing', ARRAY['marketing', 'promotion', 'growth']);

-- =====================================================
-- VIEWS FOR ANALYTICS
-- =====================================================

-- Trending products view
CREATE VIEW trending_products AS
SELECT 
    p.id,
    p.name,
    p.price,
    p.views_count,
    p.sold_quantity,
    p.rating,
    s.name as shop_name,
    c.name as category_name,
    pi.image_url as main_image
FROM products p
JOIN shops s ON p.shop_id = s.id
JOIN categories c ON p.category_id = c.id
LEFT JOIN product_images pi ON p.id = pi.product_id AND pi.is_primary = TRUE
WHERE p.is_active = TRUE
ORDER BY p.views_count DESC, p.sold_quantity DESC;

-- Top shops view
CREATE VIEW top_shops AS
SELECT 
    s.id,
    s.name,
    s.followers_count,
    s.products_count,
    s.total_sales,
    s.rating,
    c.name as category_name,
    si.image_url as logo_url
FROM shops s
JOIN categories c ON s.category_id = c.id
LEFT JOIN shop_images si ON s.id = si.shop_id AND si.is_primary = TRUE
WHERE s.is_active = TRUE
ORDER BY s.total_sales DESC, s.followers_count DESC;

-- Popular creators view
CREATE VIEW popular_creators AS
SELECT 
    cr.id,
    cr.username,
    cr.display_name,
    cr.followers_count,
    cr.videos_count,
    cr.engagement_rate,
    c.name as category_name,
    cri.image_url as profile_image
FROM creators cr
JOIN categories c ON cr.category_id = c.id
LEFT JOIN creator_images cri ON cr.id = cri.creator_id AND cri.is_primary = TRUE
WHERE cr.is_active = TRUE
ORDER BY cr.followers_count DESC, cr.engagement_rate DESC; 