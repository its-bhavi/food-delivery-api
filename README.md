# 🍕 Food Delivery API - Django REST Framework

Modern food delivery platform with Django REST API backend and Railway.app deployment.

## 🚀 Live Deployment

- **API URL:** https://food-delivery-api-production-1d00.up.railway.app
- **Frontend:** https://lightskyblue-ostrich-354680.hostingersite.com

## 📋 Features

### Customer Features
- ✅ Browse restaurants and menus
- ✅ Add items to cart
- ✅ Place orders (COD & Online Payment)
- ✅ Live order tracking with GPS
- ✅ Order history

### Restaurant/Vendor Features
- ✅ Restaurant profile management
- ✅ Menu item management (CRUD)
- ✅ Order management dashboard
- ✅ Accept/reject orders
- ✅ Update order status (Preparing → Ready)
- ✅ View customer delivery location

### Delivery Partner Features
- ✅ Delivery partner profile
- ✅ Available orders view
- ✅ Accept delivery requests
- ✅ Live GPS tracking
- ✅ Mark orders as delivered
- ✅ Navigation to restaurant/customer

### Admin Features
- ✅ User management
- ✅ Restaurant approval
- ✅ Order monitoring
- ✅ Analytics dashboard

## 🛠️ Tech Stack

**Backend:**
- Django 5.2.7
- Django REST Framework 3.15.2
- PostgreSQL (Railway)
- JWT Authentication (djangorestframework-simplejwt)
- Razorpay Payment Integration
- Google Maps API

**Deployment:**
- Railway.app (Backend API)
- PostgreSQL Database (Railway)
- Media Storage (Railway)
- WordPress/Elementor (Frontend)

## 📁 Project Structure

```
food_delivery_api/
├── delivery/              # Delivery partner app
├── food_delivery_api/     # Main project settings
├── frontend_pages/        # HTML templates for WordPress
├── media/                 # Uploaded images (restaurants, menu items)
├── orders/                # Order management app
├── users/                 # User authentication & profiles
├── vendors/               # Restaurant/vendor management
├── manage.py
├── requirements.txt
├── Procfile               # Railway deployment config
├── railway.json
└── runtime.txt
```

## 🔧 Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/its-bhavi/food-delivery-api.git
cd food-delivery-api
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create `.env` file:
```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=your-database-url
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret
GOOGLE_MAPS_API_KEY=your-google-maps-key
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### 5. Run Migrations
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

API will be available at: `http://localhost:8000/api/`

## 📡 API Endpoints

### Authentication
- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login & get JWT tokens
- `POST /api/users/token/refresh/` - Refresh access token
- `GET /api/users/profile/` - Get user profile

### Restaurants
- `GET /api/vendors/restaurants/` - List all restaurants
- `GET /api/vendors/restaurants/{id}/` - Restaurant details
- `GET /api/vendors/restaurants/{id}/menu/` - Restaurant menu
- `POST /api/vendors/profile/` - Create restaurant profile (Auth required)
- `PUT /api/vendors/profile/` - Update restaurant profile (Auth required)

### Menu Items
- `GET /api/vendors/menu-items/` - List menu items
- `POST /api/vendors/menu-items/` - Add menu item (Vendor only)
- `PUT /api/vendors/menu-items/{id}/` - Update menu item (Vendor only)
- `DELETE /api/vendors/menu-items/{id}/` - Delete menu item (Vendor only)

### Orders
- `POST /api/orders/create/` - Create new order
- `GET /api/orders/customer-orders/` - Customer's orders
- `GET /api/orders/vendor-orders/` - Vendor's orders
- `GET /api/orders/delivery-orders/` - Delivery partner's orders
- `PATCH /api/orders/{id}/update-status/` - Update order status
- `GET /api/orders/{id}/tracking/` - Live order tracking

### Delivery
- `POST /api/delivery/profile/` - Create delivery partner profile
- `PATCH /api/orders/{id}/update-location/` - Update GPS location

### Payments
- `POST /api/payments/create-razorpay-order/` - Create Razorpay order
- `POST /api/payments/verify-payment/` - Verify payment

## 🚂 Railway Deployment

### Environment Variables (Set in Railway Dashboard)
```
DEBUG=False
SECRET_KEY=<your-production-secret>
ALLOWED_HOSTS=*.railway.app,lightskyblue-ostrich-354680.hostingersite.com
RAZORPAY_KEY_ID=<your-key>
RAZORPAY_KEY_SECRET=<your-secret>
GOOGLE_MAPS_API_KEY=<your-api-key>
CORS_ALLOWED_ORIGINS=https://lightskyblue-ostrich-354680.hostingersite.com
```

DATABASE_URL is automatically set by Railway PostgreSQL plugin.

### Deployment Steps
1. Connect GitHub repository to Railway
2. Add PostgreSQL database service
3. Set environment variables
4. Deploy automatically on git push

## 📱 Frontend Pages (WordPress Integration)

Frontend HTML files in `frontend_pages/`:
- `FIXED_1_restaurant_profile.html` - Restaurant registration/profile
- `FIXED_2_delivery_partner_profile.html` - Delivery partner registration
- `FIXED_3_customer_tracking.html` - Live order tracking
- `FIXED_4_restaurant_dashboard.html` - Restaurant order management
- `FIXED_5_delivery_partner_dashboard.html` - Delivery partner dashboard
- `FIXED_restaurants_list_page.html` - Browse restaurants
- `FIXED_login_page.html` - User login

Upload these to WordPress Elementor pages.

## 🔐 Authentication Flow

1. User registers via `/api/users/register/`
2. Login at `/api/users/login/` → Receive access & refresh tokens
3. Include token in headers: `Authorization: Bearer <access_token>`
4. Refresh token when expired: `/api/users/token/refresh/`

## 📊 Database Schema

**User Types:**
- Customer
- Vendor (Restaurant Owner)
- Delivery Partner

**Main Models:**
- User (Django built-in)
- UserProfile (Optional - user_type, phone, etc.)
- Restaurant (Vendor's restaurant)
- MenuItem (Restaurant menu items)
- Order (Customer orders)
- OrderItem (Order line items)
- DeliveryPartner (Delivery partner profile)

## 🗺️ Google Maps Integration

Features using Google Maps API:
- Restaurant location selection
- Delivery address geocoding
- Live delivery tracking
- Navigation to customer/restaurant

## 💳 Payment Integration

- **COD (Cash on Delivery)** - No payment processing
- **Online Payment** - Razorpay integration
  - Create order → Get Razorpay order ID
  - Frontend handles payment UI
  - Verify payment signature on backend

## 📝 Recent Fixes & Updates

✅ Removed UserProfile dependency - Resource-based authorization
✅ Fixed 401/403 authentication errors
✅ Fixed menu item creation (boolean/price conversion)
✅ Added proper Railway media URL handling
✅ Improved error handling in tracking page
✅ Added Google Maps fallback for ad blockers
✅ Fixed GPS location tracking
✅ Database persistence optimizations

## 📚 Documentation

- `FIXES_SUMMARY.md` - All bug fixes and solutions
- `RAILWAY_DATABASE_PERSISTENCE.md` - Database setup guide
- `RAILWAY_MEDIA_SETUP.md` - Media file handling
- `RAILWAY_SETUP_GUIDE.md` - Complete deployment guide
- `WORDPRESS_INTEGRATION_GUIDE.md` - Frontend integration

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

This project is private and maintained by its-bhavi.

## 👨‍💻 Developer

**GitHub:** [@its-bhavi](https://github.com/its-bhavi)

## 🐛 Known Issues & Solutions

### Google Maps Deprecation Warnings
- **Status:** Informational only
- **Impact:** None - Maps work perfectly
- **Action:** Can update to AdvancedMarkerElement later

### Ad Blocker Blocking Maps API
- **Status:** Fixed with fallback
- **Solution:** Dashboard loads even if maps blocked
- **User Action:** Disable ad blocker for best experience

### GPS Location Not Working
- **Requirement:** HTTPS only (WordPress is HTTPS ✅)
- **User Action:** Allow browser location permission
- **Status:** Working correctly

## 🎯 Future Enhancements

- [ ] Real-time order notifications (WebSockets)
- [ ] Advanced restaurant search & filters
- [ ] Customer reviews & ratings
- [ ] Promo codes & discounts
- [ ] Multi-language support
- [ ] Push notifications
- [ ] Analytics dashboard improvements

---

**Last Updated:** November 26, 2025
**Version:** 1.0.0
**Status:** Production Ready ✅
