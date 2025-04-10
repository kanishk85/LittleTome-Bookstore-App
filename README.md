# 📚 LittleTome - Full-Featured Bookstore System

**LittleTome** is a fully functional and refined bookstore system built using Python and MySQL.  
It combines a clean user interface with robust backend operations to simulate a real-world online bookstore experience.

## 🌟 Features

- 🛍️ Browse and purchase books from multiple categories
- 🛒 Shopping cart with real-time updates
- 🎟️ Coupon code discounts applied at checkout
- 🔐 OTP-based purchase verification
- 📧 Email invoice sent to customers with proper formatting and personalized details
- 📜 View full purchase history
- 🗃️ MySQL-powered database structure with organized tables for books, users, coupons, and orders

## 🛠️ Technologies Used

- Python (UI logic and backend)
- MySQL (database)
- SMTP (for email billing)
- Environment variables for DB config (secure deployment)
- 🎨 UI designed in Figma and implemented using Tkinter Canvas for a clean, custom look

## 📂 Modules and Structure

- `window.py` – Main UI and logic handler
- `allsqldata()` – Initializes database, creates and fills tables
- OTP and email integration modules
- Separate databases for user data and purchase details

⚙️ Setup Instructions
🔧 Install dependencies:
```bash
pip install -r requirements.txt
```

🐬 MySQL required – app auto-creates DB & tables on first run. Make sure MySQL is installed & running.

📁 Create a .env file in the root folder with:
```env
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
API_KEY=your_email_api_key
SENDER_EMAIL=your_email@example.com
```
📧 Use your email API key, not your personal email password.

---

# LittleTome-Ecommerce-App


