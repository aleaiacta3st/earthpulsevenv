import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("🌍 Earth Pulse")

# Fetch data from API
try:
    response = requests.get("http://localhost:8000/alerts?limit=50")
    data = response.json()
    
    if data:
        df = pd.DataFrame(data)
        
        # Show metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Earthquakes", len(df))
        col2.metric("Avg Magnitude", f"{df['magnitude'].mean():.2f}")
        col3.metric("Max Magnitude", f"{df['magnitude'].max():.2f}")
        
        # Create map
        st.subheader("Earthquake Map")
        m = folium.Map(location=[20, 0], zoom_start=2)
        
        for idx, row in df.iterrows():
            # Color based on magnitude
            if row['magnitude'] < 2.5:
                color = 'green'
            elif row['magnitude'] < 4.5:
                color = 'orange'
            else:
                color = 'red'
            
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=row['magnitude'] * 2,
                popup=f"{row['place']}<br>Magnitude: {row['magnitude']}<br>Depth: {row['depth']} km",
                color=color,
                fill=True,
                fillColor=color
            ).add_to(m)
        
        st_folium(m, width=700, height=500)
        
        # Show data table
        st.subheader("Recent Earthquakes")
        st.dataframe(df[['place', 'magnitude', 'depth', 'occurred_at']], 
                     use_container_width=True)
    else:
        st.error("No data available")
        
except Exception as e:
    st.error(f"Cannot connect to API. Make sure it's running on port 8000")
    st.error(f"Error: {e}")