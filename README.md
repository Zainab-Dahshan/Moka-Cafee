# Moka Cafe - Modern Coffee Shop Website

A comprehensive web application for Moka Cafe, a modern coffee shop that offers an exceptional online ordering experience. Built with Flask and Bootstrap 5, this platform enables customers to browse menus, place orders, and enjoy a seamless digital experience while allowing cafe management to efficiently handle operations.

![Moka Cafe Screenshot](app/static/images/logo.png)

## 🌟 Features

- **Responsive Design**: Looks great on all devices
- **Online Ordering**: Customers can browse the menu and place orders
- **Admin Dashboard**: Manage menu items and view orders
- **Modern UI**: Clean and intuitive interface with smooth animations
- **Secure Authentication**: Admin login system
- **Image Upload**: Add and manage menu item images

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/Moka-Cafe.git
   cd Moka-Cafe
   ```

2. **Create and activate a virtual environment**

   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:

   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///cafe.db
   ```

5. **Initialize the database**

   ```bash
   flask db upgrade
   ```

6. **Run the development server**

   ```bash
   python run.py
   ```

7. **Access the application**
   - Website: [http://localhost:8000](http://localhost:8000)
   - Admin Panel: [http://localhost:8000/admin/login](http://localhost:8000/admin/login)
     - Username: `admin`
     - Password: `admin123` (change this in production)

## 📂 Project Structure

```plaintext
cafeluxe/
├── app/
│   ├── __init__.py       # Application factory and extensions
│   ├── config.py         # Configuration settings
│   ├── models.py         # Database models
│   ├── routes.py         # Application routes
│   └── forms.py          # WTForms for validation
├── migrations/           # Database migrations
├── static/
│   ├── css/              # Custom styles
│   ├── js/               # JavaScript files
│   └── images/           # Images and icons
├── templates/            # HTML templates
│   ├── admin/            # Admin panel templates
│   ├── includes/         # Reusable template parts
│   └── *.html            # Main templates
├── .env                  # Environment variables
├── .gitignore
├── requirements.txt      # Development dependencies
├── requirements-prod.txt # Production dependencies
└── run.py                # Application entry point
```

## 🛠️ Deployment

### Production Deployment with Gunicorn and Nginx

1. **Install production dependencies**

   ```bash
   pip install -r requirements-prod.txt
   ```

2. **Run with Gunicorn**

   ```bash
   gunicorn --bind 0.0.0.0:8000 wsgi:app
   ```

3. **Set up Nginx** (example configuration)

   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static {
           alias /path/to/cafeluxe/static;
           expires 30d;
       }
   }
   ```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Contact

For any questions or feedback, please contact us at [your.email@example.com](mailto:your.email@example.com)

---

Made with ❤️ and ☕

© 2024 Moka Cafe. All rights reserved.
