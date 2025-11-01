import asyncio
import aiohttp
from datetime import datetime
from .config import current_config




USGS_FEED_URL = current_config["USGS_FEED_URL"]

async def fetch_earthquake_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(USGS_FEED_URL) as response:
            if response.status != 200:
                raise Exception(f"API request failed with status {response.status}")
            data = await response.json()
            return data

if __name__ == "__main__":
    async def main():
        data = await fetch_earthquake_data()
        print(data)
    
    asyncio.run(main())




    # if name == "main" Summary:

# When Python runs a file, it sets the special variable __name__ to:

# "__main__" if the file is executed directly
# The module name if the file is imported


# This pattern (if __name__ == "__main__":) creates a conditional block that only executes when the file is run directly, not when imported.
# For async code, you need this pattern because:

# await can only be used inside async functions, not at module level
# You need asyncio.run() to create an event loop and execute coroutines


# When a module is imported, Python executes all code at module level:

# Function definitions are processed
# Any executable code outside functions runs immediately
# Code inside the if-block is skipped during imports


# This pattern allows your file to serve dual purposes:

# As a reusable module for other parts of your application
# As a standalone script for testing/debugging


# data = {
#     "type": "FeatureCollection",  # Simple key-value
#     "metadata": {                  # Key with dictionary value
#         "generated": 1744363492000,
#         "url": "https://earthquake...",
#         # more key-values
#     },
#     "features": [                  # Key with list of dictionaries value
#         {                          # First earthquake dictionary
#             "type": "Feature",
#             "properties": {        # Another nested dictionary
#                 "mag": 0.63,
#                 "tsunami": 0,
#                 # more properties
#             },
#             "geometry": {          # Another nested dictionary
#                 "type": "Point",
#                 "coordinates": [-122.816, 38.831, 1.55]  # List value
#             }
#         },
#         # more earthquake dictionaries
#     ]
# }