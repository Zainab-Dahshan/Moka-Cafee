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

### Local Development Setup

1. **Clone and setup the project** (see Quick Start section above)

2. **Run the development server**

   ```bash
   python run.py
   ```

3. **Access the application**
   - Website: [http://localhost:8000](http://localhost:8000)
   - Admin Panel: [http://localhost:8000/admin/login](http://localhost:8000/admin/login)

### Production Deployment Options

#### Option 1: Heroku Deployment (Beginner-Friendly)

1. **Install Heroku CLI** and login:

   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   heroku login
   ```

2. **Create Heroku app**:

   ```bash
   heroku create your-cafe-app-name
   ```

3. **Set environment variables**:

   ```bash
   heroku config:set SECRET_KEY=your-production-secret-key
   heroku config:set FLASK_ENV=production
   ```

4. **Deploy to Heroku**:

   ```bash
   git push heroku main
   ```

5. **Initialize database**:

   ```bash
   heroku run flask db upgrade
   ```

#### Option 2: VPS/Cloud Server Deployment (DigitalOcean, AWS, etc.)

1. **Server Setup**:

   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Python and pip
   sudo apt install python3 python3-pip python3-venv -y

   # Install Nginx
   sudo apt install nginx -y
   ```

2. **Application Setup**:

   ```bash
   # Clone your repository
   git clone https://github.com/yourusername/Moka-Cafe.git
   cd Moka-Cafe

   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install production dependencies
   pip install -r requirements-prod.txt
   ```

3. **Configure Environment**:

   ```bash
   # Create .env file
   nano .env
   ```

   Add production environment variables:

   ```env
   FLASK_ENV=production
   SECRET_KEY=your-production-secret-key
   DATABASE_URL=sqlite:///cafe.db
   ```

4. **Setup Gunicorn**

   ```bash
   # Install Gunicorn
   pip install gunicorn

   # Create systemd service
   sudo nano /etc/systemd/system/moka-cafe.service
   ```

   Add service configuration:

   ```ini
   [Unit]
   Description=Moka Cafe Flask App
   After=network.target

   [Service]
   User=ubuntu
   Group=ubuntu
   WorkingDirectory=/home/ubuntu/Moka-Cafe
   Environment="PATH=/home/ubuntu/Moka-Cafe/venv/bin"
   ExecStart=/home/ubuntu/Moka-Cafe/venv/bin/gunicorn --bind 0.0.0.0:8000 wsgi:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. **Configure Nginx**:

   ```bash
   sudo nano /etc/nginx/sites-available/moka-cafe
   ```

   Add Nginx configuration:

   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /static {
           alias /home/ubuntu/Moka-Cafe/app/static;
           expires 30d;
           add_header Cache-Control "public, immutable";
       }
   }
   ```

6. **Enable and Start Services**:

   ```bash
   # Enable and start the Flask app
   sudo systemctl enable moka-cafe
   sudo systemctl start moka-cafe

   # Enable Nginx site
   sudo ln -s /etc/nginx/sites-available/moka-cafe /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx

   # Setup SSL (optional but recommended)
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d yourdomain.com
   ```

#### Option 3: Docker Deployment (Containerized)

1. **Create Dockerfile**:

   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements-prod.txt .
   RUN pip install --no-cache-dir -r requirements-prod.txt

   COPY . .

   ENV FLASK_ENV=production
   ENV SECRET_KEY=your-production-secret-key

   EXPOSE 8000

   CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]
   ```

2. **Create docker-compose.yml**:

   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - "8000:8000"
       environment:
         - FLASK_ENV=production
         - SECRET_KEY=your-production-secret-key
       volumes:
         - ./database.db:/app/database.db
         - ./app/static/uploads:/app/app/static/uploads
     nginx:
       image: nginx:alpine
       ports:
         - "80:80"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf
       depends_on:
         - web
   ```

3. **Deploy with Docker**:

   ```bash
   docker-compose up -d
   ```

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
FLASK_APP=run.py
FLASK_ENV=production  # or development
SECRET_KEY=your-very-secure-secret-key-here
DATABASE_URL=sqlite:///cafe.db  # or PostgreSQL/MySQL URL for production
MAIL_SERVER=smtp.gmail.com  # For email functionality
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Database Setup for Production

For production, consider using PostgreSQL instead of SQLite:

1. **Install PostgreSQL**:

   ```bash
   sudo apt install postgresql postgresql-contrib -y
   ```

2. **Create database and user**:

   ```sql
   sudo -u postgres psql
   CREATE DATABASE moka_cafe;
   CREATE USER cafe_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE moka_cafe TO cafe_user;
   \q
   ```

3. **Update DATABASE_URL** in `.env`**:

   ```env
   DATABASE_URL=postgresql://cafe_user:secure_password@localhost/moka_cafe
   ```

### Security Considerations

- **Change default admin credentials** immediately after deployment
- **Use HTTPS** in production (Let's Encrypt SSL certificates)
- **Set strong SECRET_KEY** for session security
- **Configure firewall** to only allow necessary ports
- **Regular backups** of the database
- **Monitor logs** for security issues

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
