# 🎯 STEP-BY-STEP GUIDE - WordPress Me Pages Kaise Upload Karein

## 📋 Pre-Requirements

✅ WordPress login credentials
✅ Elementor plugin installed
✅ 5 Fixed HTML files ready

---

## 🚀 Complete Upload Process (Step-by-Step)

### **STEP 1: Backup Old Pages (Important!)**

1. WordPress Admin → **Pages** → **All Pages**
2. Find these pages:
   - Restaurant Profile Setup
   - Delivery Partner Profile  
   - Track Order
   - Restaurant Dashboard
   - Delivery Partner Dashboard

3. **Export karein** (safety ke liye):
   - Tools → Export → Pages → Download Export File

---

### **STEP 2: Page 1 - Restaurant Profile Setup**

**2.1 - Page Open Karein:**
```
WordPress → Pages → Find "Restaurant Profile Setup"
(Agar nahi hai toh: Add New → Title: "Restaurant Profile Setup")
```

**2.2 - Edit with Elementor:**
- Click **"Edit with Elementor"** button

**2.3 - HTML Widget Add/Replace:**
- Left sidebar → Search: **"HTML"**
- Agar already HTML widget hai → Click karke edit karo
- Agar nahi hai → Drag HTML widget to page

**2.4 - Code Copy-Paste:**
1. VS Code me file open karo: `FIXED_1_restaurant_profile.html`
2. **Ctrl+A** (select all)
3. **Ctrl+C** (copy)
4. WordPress HTML widget me ja kar **Ctrl+V** (paste)
5. Widget settings check karo:
   - Padding: 0px all sides
   - Margin: 0px all sides

**2.5 - Page Settings:**
- Page Layout → **Elementor Full Width**
- Hide Title → **Yes**
- Slug → `restaurant-profile-setup`

**2.6 - Publish:**
- Click **Update** button (bottom left)
- **View Page** karke test karo

**2.7 - Test:**
- Open: `https://lightskyblue-ostrich-354680.hostingersite.com/restaurant-profile-setup/`
- Check: Map dikh raha hai?
- Check: Console me errors?
- F12 → Console → No CSP errors hone chahiye

---

### **STEP 3: Page 2 - Delivery Partner Profile**

**Repeat same process:**

1. Page: **Delivery Partner Profile**
2. Edit with Elementor
3. HTML widget add/replace
4. Code: Copy from `FIXED_2_delivery_partner_profile.html`
5. Paste in widget
6. Slug: `delivery-partner-profile-setup`
7. Update page
8. Test: `/delivery-partner-profile-setup/`

**Test Points:**
- User info showing?
- Vehicle dropdown working?
- No errors in console?

---

### **STEP 4: Page 3 - Track Order**

**Steps:**

1. Page: **Track Order**
2. Edit with Elementor
3. HTML widget
4. Code: `FIXED_3_customer_tracking.html`
5. Slug: `track-order`
6. Update
7. Test with order ID: `/track-order/?order=36`

**Test Points:**
- Map loads?
- 3 markers visible?
  - 🟢 Green (Restaurant)
  - 🟠 Orange (Delivery)
  - 🔵 Blue (Customer)
- Timeline showing?

---

### **STEP 5: Page 4 - Restaurant Dashboard**

**Steps:**

1. Page: **Restaurant Dashboard**
2. Edit with Elementor
3. HTML widget
4. Code: `FIXED_4_restaurant_dashboard.html`
5. Slug: `restaurant-dashboard`
6. Update
7. Test: `/restaurant-dashboard/`

**Test Points:**
- Stats showing?
- Filter tabs working?
- Map modal opens?
- Customer location geocoding?

---

### **STEP 6: Page 5 - Delivery Partner Dashboard**

**Steps:**

1. Page: **Delivery Partner Dashboard**
2. Edit with Elementor
3. HTML widget
4. Code: `FIXED_5_delivery_partner_dashboard.html`
5. Slug: `delivery-partner-dashboard`
6. Update
7. Test: `/delivery-partner-dashboard/`

**Test Points:**
- GPS permission popup?
- GPS status active?
- Navigation modal working?
- Orders loading?

---

## 🔍 Common Issues & Solutions

### **Issue 1: Map Not Showing**

**Problem:** Google Maps API key error

**Solution:**
```javascript
// Check console for errors
// If "RefererNotAllowedMapError", add domain to API key restrictions
```

**Steps:**
1. Google Cloud Console → APIs & Services → Credentials
2. Select API key: `AIzaSyD1v0RxpSZc4HvO5GO4dTyGfUqi89oiHI0`
3. Application restrictions → HTTP referrers
4. Add: `lightskyblue-ostrich-354680.hostingersite.com/*`

---

### **Issue 2: CSP Errors Still Coming**

**Problem:** WordPress security plugin blocking

**Solution:**
1. Plugins → Find security plugin (e.g., Wordfence, iThemes)
2. Settings → Content Security Policy
3. Add to allowlist:
   - `https://maps.googleapis.com`
   - `https://maps.gstatic.com`

---

### **Issue 3: GPS Not Working**

**Problem:** HTTPS required for geolocation

**Solution:**
- Ensure site is on HTTPS (should be by default)
- Check browser permissions
- Test in Chrome/Edge (Safari has strict policies)

---

### **Issue 4: API Calls Failing (401/403)**

**Problem:** Backend authentication error

**Solution:**
```javascript
// Check localStorage
console.log(localStorage.getItem('access_token'));

// If null or expired, login again
```

**Steps:**
1. Logout from WordPress pages
2. Login again at `/login/`
3. Check token in localStorage (F12 → Application → Local Storage)

---

## 📊 Final Testing Checklist

### **All Pages Working?**

| Page | URL | Status |
|------|-----|--------|
| Restaurant Profile | `/restaurant-profile-setup/` | [ ] ✅ |
| Delivery Profile | `/delivery-partner-profile-setup/` | [ ] ✅ |
| Track Order | `/track-order/?order=36` | [ ] ✅ |
| Restaurant Dashboard | `/restaurant-dashboard/` | [ ] ✅ |
| Delivery Dashboard | `/delivery-partner-dashboard/` | [ ] ✅ |

### **Maps Working?**

- [ ] Restaurant profile map showing
- [ ] Customer tracking 3 markers visible
- [ ] Restaurant dashboard map modal
- [ ] Delivery dashboard navigation modal

### **Forms Working?**

- [ ] Restaurant registration
- [ ] Restaurant edit
- [ ] Delivery partner registration
- [ ] Delivery partner edit

### **Live Features Working?**

- [ ] GPS tracking sending location
- [ ] Customer tracking auto-refresh (10s)
- [ ] Restaurant dashboard auto-refresh (30s)
- [ ] Delivery dashboard GPS updates

---

## 🎯 Complete Workflow Test

**Test with real order:**

```
1. Restaurant Login
   → Go to /restaurant-profile-setup/
   → Create restaurant with map location
   → Save ✅

2. Delivery Partner Login
   → Go to /delivery-partner-profile-setup/
   → Create profile with vehicle details
   → Save ✅

3. Customer Places Order
   → Add items to cart
   → Checkout
   → Order created (Pending)

4. Restaurant Dashboard
   → Login as restaurant
   → See pending order
   → Click "Accept Order" → Confirmed
   → Click "Start Preparing" → Preparing
   → Click "Mark Ready" → Ready ✅

5. Delivery Dashboard
   → Login as delivery partner
   → See ready order
   → Allow GPS permission
   → Click "Accept Delivery" → Picked
   → GPS automatically sends location ✅

6. Customer Tracking
   → Open /track-order/?order=36
   → See 3 markers on map
   → Watch delivery partner marker move (orange)
   → Timeline updates
   → See delivery partner info ✅

7. Delivery Complete
   → Delivery dashboard
   → Click "Mark Delivered"
   → Order status: Delivered ✅
```

---

## 📞 Help & Support

**Agar koi issue ho toh:**

1. **Screenshots lo:**
   - Page ka full screenshot
   - Console errors (F12 → Console tab)

2. **Check karein:**
   - Backend API live hai? (Render dashboard)
   - API URL sahi hai code me?
   - Google Maps API key valid hai?

3. **Debug steps:**
```javascript
// Console me ye commands run karo
console.log('Token:', localStorage.getItem('access_token'));
console.log('API Base:', 'https://food-delivery-api-fr4f.onrender.com/api');
console.log('Google Maps loaded?', typeof google !== 'undefined');
```

---

## ✅ Success Criteria

**Sab kuch sahi hai agar:**

✅ All 5 pages load without errors
✅ Google Maps visible on all map pages
✅ No CSP errors in console
✅ Restaurant can register + edit profile
✅ Delivery partner can register + edit
✅ Customer tracking shows 3 markers
✅ Restaurant dashboard map modal works
✅ Delivery dashboard GPS tracking works
✅ Complete order flow: Pending → Delivered

---

**Happy Testing! 🎉**

**Koi problem ho toh screenshots ke saath report karna.** 🚀
