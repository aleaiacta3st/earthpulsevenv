from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from quake_ingest.db import get_earthquakes
import asyncio
from alerts_api.models import Earthquake
import os


app=FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"} 

@app.get("/alerts")
async def alerts(limit: int = 10, offset: int = 0, min_magnitude: float = 0):
    results = await get_earthquakes(limit, offset, min_magnitude)
    return results

from datetime import datetime, timedelta

@app.get("/latest")
async def get_latest():
    results = await get_earthquakes(limit=20)
    return {
        "retrieved_at": datetime.now().isoformat(),
        "earthquakes": results,
        "count": len(results)
    }


@app.get("/stats")
async def get_stats():
    from sqlalchemy import func, select
    from quake_ingest.db import async_session, Earthquake
    
    async with async_session() as session:
        total_count = await session.scalar(select(func.count(Earthquake.id)))
        avg_magnitude = await session.scalar(select(func.avg(Earthquake.magnitude)))
        max_magnitude = await session.scalar(select(func.max(Earthquake.magnitude)))
        latest_quake = await session.scalar(select(func.max(Earthquake.occurred_at)))
        
    return {
        "system_health": "operational",
        "database_stats": {
            "total_earthquakes": total_count,
            "average_magnitude": round(avg_magnitude, 2) if avg_magnitude else 0,
            "max_magnitude": max_magnitude or 0,
            "latest_earthquake": latest_quake.isoformat() if latest_quake else None
        },
        "api_version": "1.0.0",
        "uptime_hours": 24
    }





#API is a code on a server. This can access functions in db.py.
# FastAPI is a Python class
# When you write app = FastAPI(), you're creating an instance of the FastAPI class that becomes your unique application with its own routes, settings, and behavior.

#what is pydantic?
# Pydantic is a data validation library that works with your Python type annotations. It serves several key purposes in your FastAPI application:

# Data Validation: It ensures data coming into your API follows your defined structure
# Serialization: It handles converting between Python objects and JSON
# Documentation: It automatically generates API documentation

# So the complete data flow in the application is:

# USGS API (JSON) → Python dictionaries (parser.py) → SQLAlchemy objects → Database rows (PostgreSQL)

# And when retrieving:

# Database rows → SQLAlchemy objects → JSON (via your API)

# Health Endpoint Summary
# The /health endpoint is a standard API feature that:

# Provides a simple way to check if the service is alive and responding to requests
# Returns a 200 HTTP status code with a JSON response like {"status": "ok"} when the service is running normally
# Enables monitoring systems, load balancers, and orchestration tools to verify service availability
# Serves as the simplest form of application observability
# Often extended in production to include deeper checks (database connectivity, dependent services status)


# The uvicorn main:app --reload command breaks down like this:

# uvicorn: The web server specifically designed for Python async frameworks like FastAPI
# main:app: This specifies where to find your application:

# main is the Python file name (main.py) without the extension
# The colon : separates the file name from the variable name
# app is the variable name of your FastAPI instance inside that file


# --reload: An optional flag that makes the server automatically restart whenever you save changes to your code files, which is extremely helpful during development

# In essence, this command tells Uvicorn to run your FastAPI application and keep watching for any code changes to automatically refresh the server without you needing to restart it manually.