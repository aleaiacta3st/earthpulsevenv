import asyncio
from datetime import datetime
from .fetcher import fetch_earthquake_data

def parse_data(data):
    earthquakes_imp=[]
    features = data.get("features", [])
    for feature in features:
        container={}
        container["id"]=feature["id"]
        container["place"]=feature["properties"]["place"]
        container["magnitude"]=feature["properties"]["mag"]
        container["depth"]=feature["geometry"]["coordinates"][2]
        container["latitude"]=feature["geometry"]["coordinates"][1]
        container["longitude"]=feature["geometry"]["coordinates"][0]
        container["tsunami"]=feature["properties"]["tsunami"]
        timestamp=int(feature["properties"]["time"])
        date_time=datetime.fromtimestamp(timestamp/1000)
        container["occurred_at"]=date_time
        earthquakes_imp.append(container)
    return earthquakes_imp

if __name__=="__main__":
    async def test_parser():
        raw_data = await fetch_earthquake_data()
        parsed_data = parse_data(raw_data)
        print(f"Total earthquakes parsed: {len(parsed_data)}")
        print(f"First earthquake: {parsed_data[0]}")
    
    asyncio.run(test_parser())








# The features array contains individual earthquake objects. Each individual feature (earthquake) in the features array has 4 top-level keys: type, properties, geometry, id.
# The line features = data.get("features", []) is retrieving the "features" array from your data dictionary using a safer method than direct indexing.
# Here's what it does:

# It looks for the key "features" in the data dictionary
# If the key exists, it returns the value (the array of earthquake features)
# If the key doesn't exist, it returns the default value (an empty list [])

# This is safer than using features = data["features"] because:

# If "features" isn't in the dictionary, data["features"] would raise a KeyError
# The .get() method gracefully handles missing keys by returning the default value

# The empty list [] as a default value means your code won't break even if the data is malformed or doesn't contain earthquake features - you'd just process an empty list.
# This defensive programming approach makes your parser more robust against unexpected data formats or API changes.