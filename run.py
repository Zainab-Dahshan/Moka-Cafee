from app import create_app
from waitress import serve
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == "__main__":
    try:
        logger.info("Starting Moka Cafe server on http://0.0.0.0:8000")
        logger.info("Press Ctrl+C to stop the server")
        serve(
            app,
            host='0.0.0.0', 
            port=8000,
            threads=4  # Adjust based on your server's CPU cores
        )
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

