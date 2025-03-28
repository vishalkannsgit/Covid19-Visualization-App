import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("covid_19_india.csv", parse_dates=["Date"], dayfirst=True)
    df = df.rename(columns={
        "State/UnionTerritory": "State",
        "Cured": "Recovered",
        "Deaths": "Death",
        "Confirmed": "Confirmed"
    })
    return df

df = load_data()

# Dictionary for State Coordinates
state_coords = {
    "Andhra Pradesh": [15.9129, 79.7400], "Arunachal Pradesh": [28.2180, 94.7278], "Assam": [26.2006, 92.9376],
    "Bihar": [25.0961, 85.3131], "Chhattisgarh": [21.2787, 81.8661], "Goa": [15.2993, 74.1240],
    "Gujarat": [22.2587, 71.1924], "Haryana": [29.0588, 76.0856], "Himachal Pradesh": [31.1048, 77.1734],
    "Jharkhand": [23.6102, 85.2799], "Karnataka": [15.3173, 75.7139], "Kerala": [10.8505, 76.2711],
    "Madhya Pradesh": [22.9734, 78.6569], "Maharashtra": [19.7515, 75.7139], "Manipur": [24.6637, 93.9063],
    "Meghalaya": [25.4670, 91.3662], "Mizoram": [23.1645, 92.9376], "Nagaland": [26.1584, 94.5624],
    "Odisha": [20.9517, 85.0985], "Punjab": [31.1471, 75.3412], "Rajasthan": [27.0238, 74.2179],
    "Sikkim": [27.5330, 88.5122], "Tamil Nadu": [11.1271, 78.6569], "Telangana": [18.1124, 79.0193],
    "Tripura": [23.9408, 91.9882], "Uttar Pradesh": [26.8467, 80.9462], "Uttarakhand": [30.0668, 79.0193],
    "West Bengal": [22.9868, 87.8550], "Delhi": [28.7041, 77.1025], "Jammu and Kashmir": [33.7782, 76.5762],
    "Ladakh": [34.1526, 77.5770], "Puducherry": [11.9416, 79.8083], "Chandigarh": [30.7333, 76.7794]
}

# Add Latitude & Longitude
df["Latitude"] = df["State"].map(lambda x: state_coords.get(x, [None, None])[0])
df["Longitude"] = df["State"].map(lambda x: state_coords.get(x, [None, None])[1])

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Overview", "COVID-19 Dashboard", "Comparison Chart", "COVID-19 Map", "SMA Forecast", "Time-Lapse Map", "How to Use & Tools"])


# Overview Page
if page == "Overview":
    st.title("COVID-19 Data Analysis for India")
    st.image("giphy.gif", caption="COVID-19 Spread Animation", use_container_width=True)
    st.write("""
    ## About This Project
    This project provides an interactive dashboard for visualizing COVID-19 cases in India.
    
    ### Project Objective
    - Analyze and visualize COVID-19 case trends across different states in India.
    - Allow users to interactively explore data to understand the impact of the pandemic.

    ### Technologies & Tools Used
    - **Python** (Data Processing)
    - **Pandas** (Data Manipulation)
    - **Streamlit** (Interactive UI)
    - **Plotly** (Visualization)
    - **Folium** (Mapping)

    ### Features:
    - 📊 **Dashboard**: View trends in confirmed, recovered, and death cases.
    - 🌍 **Interactive Map**: See COVID-19 impact per state.
    - 📈 **SMA Forecast**: Predict short-term COVID-19 trends using a simple moving average.
    """)
elif page == "How to Use & Tools":
    st.title("📖 How to Use This Application & Key Concepts")

    # Section: How to Use
    st.header("🔹 How to Use This Application")
    st.write("""
    Follow these steps to explore COVID-19 trends in India:
    
    1. **Overview Page** - Learn about the project and the technologies used.
    2. **COVID-19 Dashboard** - Select a state to see the confirmed, recovered, and death cases over time.
    3. **Comparison Chart** - Compare COVID-19 trends between two states using a visual chart.
    4. **COVID-19 Map** - View an interactive map showing COVID-19 spread across states.
    5. **SMA Forecast** - Predict COVID-19 case trends using a **Simple Moving Average (SMA)**.
    6. **Time-Lapse Map** - Watch the spread of COVID-19 over time in India using an animated map.

    📌 **Navigate using the sidebar menu** to explore different sections!
    """)

    # Section: Key Concepts
    st.header("📊 Key Concepts Explained")

    # 1. Simple Moving Average (SMA)
    st.subheader("🔹 Simple Moving Average (SMA)")
    st.write("""
    - **SMA** is a statistical method used to smoothen data and observe trends over time.
    - It calculates the average of the last 'n' days of COVID-19 cases to predict the trend.
    - **Formula for SMA**:
        ```
        SMA(n) = (X1 + X2 + X3 + ... + Xn) / n
        ```
        where **X1, X2, ..., Xn** are the number of cases in the last 'n' days.
    - This helps in understanding the COVID-19 case trend and predicting future cases.

    **Example in Python Code:**
    ```python
    df_state["SMA_7"] = df_state["Confirmed"].rolling(window=7).mean()
    ```
    """)

    # 2. State-wise COVID-19 Comparison
    st.subheader("🔹 Comparing COVID-19 Trends Between Two States")
    st.write("""
    - The **Comparison Chart** allows users to compare COVID-19 cases across two selected states.
    - It uses **line charts** to visually analyze differences in **confirmed, recovered, and death cases**.
    - **How It Works?**
      - You select two states.
      - The app fetches the latest data for those states.
      - A **dual-line graph** is displayed to compare trends.
    - **Example Visualization Code:**
    ```python
    fig.add_trace(go.Scatter(x=df_state1["Date"], y=df_state1["Confirmed"], mode="lines", name=f"{state_1} - Confirmed"))
    fig.add_trace(go.Scatter(x=df_state2["Date"], y=df_state2["Confirmed"], mode="lines", name=f"{state_2} - Confirmed"))
    ```
    """)

    # 3. Interactive Map Visualization
    st.subheader("🔹 Interactive Map for COVID-19 Cases")
    st.write("""
    - This feature uses **Folium** to display an interactive map.
    - Each state is represented by a **red circle** where the size indicates the number of confirmed cases.
    - Clicking on a state shows its total **confirmed cases and deaths**.
    - **How It Works?**
      - The app extracts the latest COVID-19 data.
      - It assigns **latitude and longitude** for each state.
      - The **Folium map** generates markers for each state.

    **Example Code for Map:**
    ```python
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=max(5, row["Confirmed"] / 50000),
        color="red",
        fill=True,
        fill_color="red",
        popup=f"{row['State']}: {row['Confirmed']} cases, {row['Death']} deaths"
    ).add_to(india_map)
    ```
    """)

    # 4. COVID-19 Dashboard Overview
    st.subheader("🔹 COVID-19 Dashboard")
    st.write("""
    - Displays trends for **Confirmed, Recovered, and Death** cases.
    - Uses **line graphs** from Plotly to show how cases evolved over time in a selected state.
    - Helps users track the impact of COVID-19 and observe peaks & declines.

    **Example Code for Dashboard Graph:**
    ```python
    fig = px.line(df_state, x="Date", y=["Confirmed", "Recovered", "Death"], title=f"Trend of COVID-19 in {state}")
    ```
    """)

    # Section: Technologies Used
    st.header("🛠️ Technologies & Libraries Used")
    st.write("""
    - **Python**: Core programming language for data processing.
    - **Pandas**: Data manipulation and cleaning.
    - **Streamlit**: Builds an interactive web application.
    - **Plotly**: Creates interactive charts for data visualization.
    - **Folium**: Generates interactive maps for geographic analysis.
    - **Jupyter Notebook**: Used for initial data analysis before building the app.
    """)

    st.success("✅ You are now ready to explore the COVID-19 trends in India! Use the sidebar to navigate through different sections.")

# COVID-19 Dashboard
elif page == "COVID-19 Dashboard":
    st.title("COVID-19 Dashboard for India")
    state = st.sidebar.selectbox("Select State", df["State"].unique())
    df_state = df[df["State"] == state]
    st.subheader(f"COVID-19 Trend in {state}")
    fig = px.line(df_state, x="Date", y=["Confirmed", "Recovered", "Death"],
                  labels={"value": "Cases", "Date": "Date"}, title=f"Trend of COVID-19 in {state}")
    st.plotly_chart(fig)

# COVID-19 Map
elif page == "COVID-19 Map":
    st.title("COVID-19 Map of India")
    st.write("Select a state on the map to see confirmed cases and deaths.")
    india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    for _, row in df[df["Date"] == df["Date"].max()].iterrows():
        if pd.notna(row["Latitude"]) and pd.notna(row["Longitude"]):
            folium.CircleMarker(
                location=[row["Latitude"], row["Longitude"]],
                radius=max(5, row["Confirmed"] / 50000),
                color="red",
                fill=True,
                fill_color="red",
                popup=f"{row['State']}: {row['Confirmed']} cases, {row['Death']} deaths"
            ).add_to(india_map)
    folium_static(india_map)
elif page == "Comparison Chart":
    st.title("Compare COVID-19 Trends Between Two States")
    
    # Select two states for comparison
    state_1 = st.selectbox("Select First State", df["State"].unique(), index=0)
    state_2 = st.selectbox("Select Second State", df["State"].unique(), index=1)

    # Filter data for selected states
    df_state1 = df[df["State"] == state_1]
    df_state2 = df[df["State"] == state_2]

    # Ensure valid indexing for latest data
    latest_1 = df_state1.tail(1).iloc[0]
    latest_2 = df_state2.tail(1).iloc[0]

    # Display Key Metrics Side by Side
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(state_1)
        st.metric(label="Confirmed Cases", value=f"{latest_1['Confirmed']:,}")
        st.metric(label="Recovered Cases", value=f"{latest_1['Recovered']:,}")
        st.metric(label="Deaths", value=f"{latest_1['Death']:,}")
    
    with col2:
        st.subheader(state_2)
        st.metric(label="Confirmed Cases", value=f"{latest_2['Confirmed']:,}")
        st.metric(label="Recovered Cases", value=f"{latest_2['Recovered']:,}")
        st.metric(label="Deaths", value=f"{latest_2['Death']:,}")

    # Create a combined figure for trends
    fig = go.Figure()

    # Add traces for State 1
    fig.add_trace(go.Scatter(x=df_state1["Date"], y=df_state1["Confirmed"], mode="lines", name=f"{state_1} - Confirmed", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=df_state1["Date"], y=df_state1["Recovered"], mode="lines", name=f"{state_1} - Recovered", line=dict(color="green")))
    fig.add_trace(go.Scatter(x=df_state1["Date"], y=df_state1["Death"], mode="lines", name=f"{state_1} - Deaths", line=dict(color="red")))

    # Add traces for State 2
    fig.add_trace(go.Scatter(x=df_state2["Date"], y=df_state2["Confirmed"], mode="lines", name=f"{state_2} - Confirmed", line=dict(dash="dash", color="blue")))
    fig.add_trace(go.Scatter(x=df_state2["Date"], y=df_state2["Recovered"], mode="lines", name=f"{state_2} - Recovered", line=dict(dash="dash", color="green")))
    fig.add_trace(go.Scatter(x=df_state2["Date"], y=df_state2["Death"], mode="lines", name=f"{state_2} - Deaths", line=dict(dash="dash", color="red")))

    # Set layout
    fig.update_layout(title=f"COVID-19 Comparison: {state_1} vs {state_2}",
                      xaxis_title="Date",
                      yaxis_title="Cases",
                      legend_title="Legend",
                      template="plotly_dark")

    # Display the chart
    st.plotly_chart(fig)

# Time-Lapse Map
elif page == "Time-Lapse Map":
    st.title("COVID-19 Spread Over Time in India")
    st.write("This animation shows the growth of COVID-19 cases across states over time.")
    df_sorted = df.sort_values(by="Date")
    fig = px.scatter_geo(df_sorted, lat="Latitude", lon="Longitude", size="Confirmed", animation_frame=df_sorted["Date"].astype(str),
                          hover_name="State", title="Time-Lapse of COVID-19 Spread in India", projection="natural earth")
    st.plotly_chart(fig)

# SMA Forecast
elif page == "SMA Forecast":
    st.title("COVID-19 Trend Prediction (SMA)")
    state = st.selectbox("Select State for Forecast", df["State"].unique())
    df_state = df[df["State"] == state].copy()
    df_state["SMA_7"] = df_state["Confirmed"].rolling(window=7).mean()
    st.subheader(f"7-Day Moving Average Prediction for {state}")
    fig = px.line(df_state, x="Date", y=["Confirmed", "SMA_7"],
                  labels={"value": "Cases", "Date": "Date"},
                  title=f"Predicted Trend in {state} (SMA)")
    fig.update_traces(marker=dict(size=3))
    st.plotly_chart(fig)
