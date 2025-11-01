import os
from pathlib import Path #Better file path handling than string manipulation
from dotenv import load_dotenv 

#first half is the path to the current parent
#.parent goes one level up to find .env file
BASE_DIR =Path(__file__).parent.parent  

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

#store config values in .env. loaddotenv. Reads from .env. loads them into os.environ 

ENV = os.environ.get("APP_ENV", "development")


# Configuration dictionary with settings for different environments
config = {
    "development": {
        "DATABASE_URL": f"postgresql+asyncpg://postgres:{os.environ.get('DB_PASSWORD')}@localhost:5432/Earthquakes",
        "USGS_FEED_URL": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson",
        "POLL_INTERVAL": 300  # 5 minutes in seconds
    },
    "testing": {
        "DATABASE_URL": f"postgresql+asyncpg://postgres:{os.environ.get('DB_PASSWORD')}@localhost:5432/Earthquakes_Test",
        "USGS_FEED_URL": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson",
        "POLL_INTERVAL": 60  # Faster polling for tests
    },
    "production": {
        "DATABASE_URL": f"postgresql+asyncpg://postgres:{os.environ.get('DB_PASSWORD')}@db.render.com:5432/Earthquakes_Prod",
        "USGS_FEED_URL": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson",
        "POLL_INTERVAL": 300
    }
}

current_config = config[ENV]


# The production DATABASE_URL uses 'db.render.com' as a placeholder
# When actually deploying to Render.com:
# 1. Render will provision a PostgreSQL database with its own unique hostname
# 2. You'll need to replace this with the actual connection string from your Render dashboard
# 3. Render typically provides connection details in format: 
#    postgresql://user:password@postgres-instance-name.render.com:5432/database_name
# 4. Render also supports environment variables for secure credential management


# Environment Selection System
# ----------------------------
# This configuration uses an environment variable called APP_ENV to determine
# which set of configuration values to use. The mechanism works as follows:
#
# 1. If APP_ENV is set (in the .env file or via terminal), that value is used
#    to select configuration (e.g., "development", "testing", "production")
#
# 2. If APP_ENV is not set, it defaults to "development" for local work
#
# 3. To change environments:
#    - For local testing: Add APP_ENV=testing to .env file
#    - For production: The deployment platform (Render.com/AWS) will set APP_ENV=production
#
# This approach allows the same codebase to run in different environments without
# code changes. During deployment, the cloud platform will set APP_ENV=production
# automatically, switching to production database URLs and other settings.
#
# The line below exports only the configuration for the active environment:
#current_config = config[ENV]
