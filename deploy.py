import os
import subprocess
import sys

def install_dependencies(requirements_file):
    print(f"📦 Installing dependencies from {requirements_file} ...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "-r", requirements_file,
            "--trusted-host", "pypi.org",
            "--trusted-host", "files.pythonhosted.org"
        ])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print("❌ Error installing dependencies:", e)
        sys.exit(1)

def run_local_server():
    print("🏠 Starting local production server using Waitress...")
    try:
        # Ensure waitress is installed
        subprocess.check_call([sys.executable, "-m", "pip", "install", "waitress"])
        # Run the server
        subprocess.check_call([
            sys.executable, "-m", "waitress", "serve",
            "--port=8000",
            "wsgi:app"
        ])
    except subprocess.CalledProcessError as e:
        print("❌ Error starting server:", e)
        sys.exit(1)

def main():
    print("🍵 Moka Cafe Deployment Script")
    print("========================================")
    print("Choose deployment platform:")
    print("1. Heroku (Not supported on Windows in this script)")
    print("2. DigitalOcean App Platform (Not supported here)")
    print("3. AWS Elastic Beanstalk (Not supported here)")
    print("4. Local Production")

    choice = input("Enter your choice (1-4): ").strip()

    if choice == "4":
        print("📝 Setting up local production deployment...")
        # Install production dependencies
        req_file = "requirements.txt"  # or "requirements-prod.txt" if exists
        if not os.path.exists(req_file):
            print(f"❌ {req_file} not found! Please create it first.")
            sys.exit(1)
        install_dependencies(req_file)
        # Run server locally with Waitress
        run_local_server()
    else:
        print("❌ This script only supports Local Production (choice 4) on Windows.")
        print("Please use a Linux/macOS machine for Heroku or Gunicorn deployment.")

if __name__ == "__main__":
    main()
