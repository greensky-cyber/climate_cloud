import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px
import streamlit as st 
import random

#--------------------------------------------
# CONFIGURATION OF PAGE 
#--------------------------------------------

st.set_page_config(
    page_title="Climate Cloud Analysis",
    page_icon="🌤️",
    layout="wide"
)
#--------------------------------------------
# TITLE AND SUBHEADERS 
#--------------------------------------------

st.title("🌎Climate Cloud Analysis")
st.write("""
Climate Cloud is a climate data analysis project developed using Python to simplify the exploration and interpretation of climate datasets.
 It enables users to identify climate trends and environmental patterns through effective data processing and interactive visualizations.
""")
st.divider()


st.subheader("📑Executive Summary")
st.markdown("""
- Climate Cloud is a Python-based project developed to analyze and visualize climate data through an interactive and user-friendly interface.
- It enables users to explore and visualize the available climate dataset, perform data preprocessing, and explore important climate trends using statistical analysis.
- The project generates interactive visualizations with libraries such as Matplotlib, Seaborn, and Plotly Express, making complex climate data easier to understand.
- By transforming raw climate data into meaningful insights, Climate Cloud supports efficient data exploration and enhances understanding of environmental patterns.
""")
st.divider()

st.subheader("🧩Project Objectives")
st.markdown("""
- To analyze climate datasets and identify meaningful climate trends and environmental patterns.
- To perform data preprocessing to improve the accuracy and quality of climate data analysis.
- To examine the relationship between climate indicators such as temperature, rainfall, CO₂ concentration, sea level rise, and air quality.
- To identify climate trends and environmental patterns through exploratory data analysis and interactive visualizations.
- To generate meaningful insights using statistical analysis and graphical representations for better understanding of climate change.
- To develop an interactive and user-friendly platform that enables users to explore and visualize the available climate dataset efficiently.
""")
st.divider()

st.subheader("📊Dataset Highlights")
st.markdown("""
- **Total Records:** 1,200 climate observations.
- **Total Features:** 20 climate-related attributes.
- **Data Quality:** No missing values in the dataset.
- **Coverage:** Climate data from multiple countries across different years.
- **Key Variables:** Temperature, rainfall, CO₂ concentration, sea level rise, air quality, and climate risk indicators.
- **Purpose:** Supports climate data analysis, trend identification, and interactive visualization.
""")
st.divider()

st.subheader("✨Key Insights")
st.markdown("""
- **Temperature Trends**: The analysis indicates an overall warming trend in the selected climate observations over the analyzed years.
- **Rainfall Patterns:** Analysis shows variations in rainfall patterns across different regions and years, highlighting differences in precipitation conditions.
- **CO₂ Concentration:** The analysis shows variations and trends in CO₂ concentration across the observed countries and years, providing an important indicator for studying climate change.
- **Sea Level Rise:** The dataset includes sea-level-rise measurements that can be used to examine changes in this important climate indicator and potential coastal impacts.
- **Air Quality:** Air Quality Index values vary across countries and years, allowing users to examine regional differences in air quality alongside other climate indicators.
""" )
st.divider()

st.subheader("🎯Expected Outcomes")
st.markdown("""
- Provide a clear understanding of climate trends and environmental changes.
- Generate meaningful and interactive visualizations for climate data analysis.
- Identify relationships between important climate indicators.
- Enable users to explore datasets through statistical analysis and EDA.
- Offer a user-friendly platform for efficient climate data visualization.
""")

st.markdown("<hr style='border:2px solid #4A4A4A;'>", unsafe_allow_html=True)

st.header("📖 Project Description")

st.subheader("Problem Statement")
st.markdown("""
Climate information is often distributed across multiple environmental indicators, making it difficult to analyze regional climate patterns and
identify areas that may require greater attention. Climate Cloud addresses this problem by bringing key climate indicators into a single interactive
platform, enabling users to explore climate trends, compare regions, and assess climate-related conditions through data-driven visualizations.

The project analyzes a Climate Change Dataset containing indicators such as temperature, rainfall, CO₂ concentration, sea level rise, and climate risk 
to provide meaningful insights for:

- **Researchers**: Analyze climate trends and environmental changes over time.
- **Students**: Explore climate data through interactive visualizations and analysis.
- **Environmental Analysts**: Examine important climate indicators and regional variations.
- **Decision Makers**: Gain data-driven insights that can support environmental planning.
- **General Users**: Understand climate patterns through an accessible and interactive dashboard.
""")
st.divider()

st.subheader("📊Dataset Overview")
st.markdown("""
The dataset contains **1,200 climate observations** with **20 environmental attributes**, covering climate indicators, atmospheric conditions, and
 environmental changes across multiple countries over different years.
### Climate Information
- Year
- Country
- Global Average Temperature
- Temperature Anomaly
- Maximum and Minimum Temperature

### Environmental Indicators
- CO₂ Concentration (ppm)
- Annual Rainfall (mm)
- Sea Level Rise (mm)
- Sea Surface Temperature
- Air Quality Index (AQI)

### Climate Risk Factors
- Heatwave Days
- Drought Index
- Flood Events Count
- Forest Cover (%)
- Deforestation Rate

### Sustainability & Energy Metrics
- Fossil Fuel Consumption
- Renewable Energy Share
- Climate Risk Index
- Predicted Temperature (2050)

""")

st.markdown("<hr style='border:2px solid #4A4A4A;'>", unsafe_allow_html=True)

#-----------------------------------------
# LOAD DATASET
#-----------------------------------------

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Climate_Dataset.csv")

        # Cleaning
        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df

    except Exception as e:
        st.error(f"Error loading dataset:\n{e}")
        return None 

df = load_data()
if df is None:
    st.stop()
#------------------------------------------------
# SIDEBAR FILTERS 
#------------------------------------------------
st.sidebar.title("🌤️Climate Cloud")
st.sidebar.image(
    "https://img.icons8.com/color/96/earth-planet.png",
    width=80
)

theme = st.sidebar.selectbox(
    "🎨 Dashboard Theme",
    ["Dark", "Light"]
)

if theme == "Dark":
    plot_template = "plotly_dark"

    st.markdown("""
    <style>
    .stApp{
        background-color:#0E1117;
        color:white;
    }
    </style>
    """, unsafe_allow_html=True)

elif theme == "Light":
    plot_template = "plotly_white"

    st.markdown("""
    <style>
    .stApp{
        background-color:white;
        color:black;
    }
    </style>
    """, unsafe_allow_html=True)


st.sidebar.title("Climate Cloud")

# ============================
# 🔍 Search Country
# ============================

search_country = st.sidebar.text_input(
    "🔍 Search Country",
    placeholder="Type a country...",
    key="search_country"
)

all_countries = sorted(df["country"].dropna().unique())

countries = [
    country for country in all_countries
    if search_country.strip().lower() in str(country).lower()
]

selected_country = st.sidebar.multiselect(
    "🌍 Select Country",
    options=countries,
    default=countries,
    key="selected_country"
)

# ============================
# 🔍 Search Year
# ============================

search_year = st.sidebar.text_input(
    "🔍 Search Year",
    placeholder="Type a year, e.g. 2020...",
    key="search_year"
)

all_years = sorted(df["year"].dropna().unique())

# Search years using text, even if the column contains numbers
years = [
    year for year in all_years
    if search_year.strip() in str(year)
]

selected_year = st.sidebar.multiselect(
    "📅 Select Year",
    options=years,
    default=years,
    key="selected_year"
)

temp_range = st.sidebar.slider(
    "🌡️ Global Average Temperature",
    float(df["global_avg_temperature"].min()),
    float(df["global_avg_temperature"].max()),
    (
        float(df["global_avg_temperature"].min()),
        float(df["global_avg_temperature"].max())
    )
)

filtered_df = df[
    (df["country"].isin(selected_country)) &
    (df["year"].isin(selected_year)) &
    (df["global_avg_temperature"] >= temp_range[0]) &
    (df["global_avg_temperature"] <= temp_range[1])
]
if filtered_df.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust your filters.")
    st.stop()
    
st.markdown("---")
st.subheader("🎯 Current Filter Selection")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"🌍 Countries Selected\n\n{len(selected_country)}")

with col2:
    st.info(f"📅 Years Selected\n\n{len(selected_year)}")

with col3:
    st.info(
        f"🌡️ Temperature Range\n\n{temp_range[0]:.1f}°C - {temp_range[1]:.1f}°C"
    )

st.markdown("---")

#--------------------------------------------------
# FACTS ABOUT CLIMATE
#--------------------------------------------------
facts = [
    "🌱 Forest ecosystems play an important role in absorbing atmospheric carbon dioxide.",
    "🌍 Global temperatures have increased significantly over the long term.",
    "🌊 Sea-level rise is an important indicator of climate change.",
    "☀️ Renewable energy can help reduce dependence on fossil fuels.",
    "🌳 Forest conservation supports carbon storage and ecosystem health."
]
st.sidebar.markdown("---")
st.sidebar.subheader("🌍 Climate Fact")

st.sidebar.success(random.choice(facts))

st.sidebar.write(f"📄 Records : {len(filtered_df)}")
st.sidebar.write(f"🌍 Countries : {filtered_df['country'].nunique()}")
st.sidebar.write(f"📅 Years : {filtered_df['year'].nunique()}")

st.sidebar.markdown("---")
st.sidebar.subheader("⚙ Technologies Used")

with st.sidebar.expander("🐍 Python"):
    st.write("""
**Role:** Main Programming Language

**Used For:**
- Developing the complete dashboard
- Writing application logic
- Processing climate data
""")

with st.sidebar.expander("📊 Pandas"):
    st.write("""
**Role:** Data Analysis Library

**Used For:**
- Reading the CSV dataset
- Filtering countries and years
- Calculating KPIs
- Grouping data for charts
""")

with st.sidebar.expander("🔢 NumPy"):
    st.write("""
**Role:** Numerical Computing Library

**Used For:**
- Mathematical calculations
- Efficient numerical operations
- Supporting data analysis
""")

with st.sidebar.expander("📈 Plotly"):
    st.write("""
**Role:** Visualization Library

**Used For:**
- Bar Chart
- Line Chart
- Scatter Plot
- Bubble Chart
- Choropleth Map
- Treemap
- Sunburst Chart
""")

with st.sidebar.expander("🌐 Streamlit"):
    st.write("""
**Role:** Dashboard Framework

**Used For:**
- Interactive web application
- Sidebar filters
- KPI Cards
- Displaying charts
- User interface
""")

st.sidebar.markdown("---")
st.sidebar.subheader("ℹ About")

st.sidebar.info(
    """
Climate Cloud is an interactive dashboard
that analyzes global climate trends
through visualizations and filtering.
"""
)
#---------------------------------------------------
# PROJECT DESCRIPTION AND DATASET OVERVIEW
#---------------------------------------------------
st.title("🌤️ Climate Cloud")

st.write("""
Welcome to **Climate Cloud**, an interactive climate data analysis dashboard developed using Python and Streamlit.
This platform enables users to explore climate datasets, analyze environmental trends, and generate meaningful insights through interactive visualizations.
""")

st.header("📂 Climate Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", filtered_df.shape[0])

with col2:
    st.metric("Total Columns", filtered_df.shape[1])

with col3:
    st.metric("Countries", filtered_df["country"].nunique())

if st.sidebar.button("🔄 Reset Filters"):
    st.session_state.clear()
    st.rerun()

st.subheader("📄Dataset Preview")
st.write("Shape:", filtered_df.shape)
st.dataframe(filtered_df, use_container_width=True)
st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Column Info",
    "📄 Dataset Preview",
    "📈 Statistics",
    "❌ Missing Values",
    "📊 Data Quality"
])

#---------------------------------------------------
# GENERAL INFORMATION 
#---------------------------------------------------
with st.expander("💡 Generate Climate Insights Based on Selected Data"):

    avg_temp = filtered_df["global_avg_temperature"].mean()
    avg_co2 = filtered_df["co2_concentration_ppm"].mean()
    avg_risk = filtered_df["climate_risk_index"].mean()

    st.success(f"""
🌡️ **Average Temperature:** {avg_temp:.2f} °C

🌱 **Average CO₂ Concentration:** {avg_co2:.2f} ppm

⚠️ **Average Climate Risk Index:** {avg_risk:.2f}

📊 These insights are automatically calculated from the currently selected
countries, years, and temperature range.
""")

    st.markdown("""
### 🔎 Interpretation

These values provide a snapshot of the climate conditions
represented by the currently selected data. Use the interactive
visualizations below to explore how these indicators vary
across countries and years.
""")
#---------------------------------------------------
# KPI CARDS
#---------------------------------------------------

st.subheader("📊 Climate Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🌡 Avg Temperature",
        f"{filtered_df['global_avg_temperature'].mean():.2f} °C"
    )

with col2:
    st.metric(
        "🌱 Avg CO₂",
        f"{filtered_df['co2_concentration_ppm'].mean():.2f} ppm"
    )

with col3:
    st.metric(
        "🌊 Avg Sea Level",
        f"{filtered_df['sea_level_rise_mm'].mean():.2f} mm"
    )

with col4:
    st.metric(
        "⚠ Avg Climate Risk",
        f"{filtered_df['climate_risk_index'].mean():.2f}"
    )

required_columns = [
    "country",
    "year",
    "global_avg_temperature",
    "co2_concentration_ppm",
    "temperature_anomaly",
    "climate_risk_index",
    "sea_level_rise_mm",
    "annual_rainfall_mm",
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        f"Dataset is missing required columns: {missing_columns}"
    )
    st.stop()
#--------------------------------------------------
# TAB 1 = COLUMN INFORMATION
#--------------------------------------------------
with tab1:

    st.subheader("📋 Column Information")

    info = pd.DataFrame({
        "Column": filtered_df.columns,
        "Data Type": filtered_df.dtypes.astype(str),
        "Non Null": filtered_df.count().values,
        "Unique Values": filtered_df.nunique().values
    })

    st.dataframe(info, use_container_width=True)

#--------------------------------------------------
# TAB 2 = DATASET PREVIEW 
#--------------------------------------------------
with tab2:

    st.subheader("📄 Dataset Preview")

    st.dataframe(filtered_df, use_container_width=True)

#--------------------------------------------------
# TAB 3 = STATISTICAL SUMMARY 
#--------------------------------------------------
with tab3:

    st.subheader("📈 Statistical Summary")

    st.dataframe(filtered_df.describe(), use_container_width=True)

#--------------------------------------------------
# TAB 4 = MISSING VALUES 
#--------------------------------------------------
with tab4:

    st.subheader("❌ Missing Values")

    missing = pd.DataFrame({
        "Missing Values": filtered_df.isnull().sum(),
        "Percentage (%)": round(filtered_df.isnull().mean()*100,2)
    })

    st.dataframe(missing)

    if missing["Missing Values"].sum()==0:
        st.success("✅ No Missing Values Found")

#--------------------------------------------------
# TAB 5 = DATA QUALITY REPORT 
#--------------------------------------------------
with tab5:

    st.subheader("📊 Data Quality Report")

    quality = pd.DataFrame({
    "Data Type": filtered_df.dtypes.astype(str),
    "Unique Values": filtered_df.nunique(),
    "Missing Values": filtered_df.isnull().sum()
})

duplicate_count = filtered_df.duplicated().sum()

st.dataframe(quality, use_container_width=True)

if duplicate_count == 0:
    st.success("✅ No duplicate rows found.")
else:
    st.warning(f"⚠️ {duplicate_count} duplicate rows found.")

    st.dataframe(quality)
st.markdown("<hr style='border:2px solid #4A4A4A;'>", unsafe_allow_html=True)

#-------------------------------------------------
#VISUALIZATIONS
#--------------------------------------------------

st.header("📈 Visualizations")

st.divider()

st.subheader("Bar Chart Representation of Average Global Temperature Across Different Countries")
country_temp = (
    filtered_df.groupby("country",as_index=False)["global_avg_temperature"].mean()
)
#--------------------------------------------------
# GRAPH 1 : BAR GRAPH
#--------------------------------------------------

fig1 = px.bar(
    country_temp,
    x="country",
    y="global_avg_temperature",
    color="country",
    color_discrete_sequence=[
        "#0B6623",
        "#228B22",
        "#2E8B57",
        "#3CB371",
        "#66CDAA",
        "#90EE90",
    ],
    text_auto=".2f",
    title="🌡️ Average Global Temperature by Country",
    hover_data={
        "country": True,
        "global_avg_temperature": ":.2f"
    }
)


fig1.update_traces(marker_line_width=1)
fig1.update_layout(
        template=plot_template,
        title_x=0.5,
        xaxis_title="Country",
        yaxis_title="Average Global Temperature",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        height=550
)
hover_data={
    "country": True,
    "global_avg_temperature": ":.2f"
}

st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
### 🌍 Key Insights
- Compares the average temperature across different countries.
- Helps identify regions experiencing higher temperatures.
- Supports the analysis of global climate variations.
- Provides useful information for environmental monitoring and sustainability studies.
- Useful for policymakers and researchers to understand climate change impacts across countries.
""")

st.divider()

#--------------------------------------------------
# GRAPH 2 : LINE GRAPH
#--------------------------------------------------

st.subheader("Line Chart Representation of Average Global Temperature Across Different Years")
year_temp = (
    filtered_df.groupby("year", as_index=False)["global_avg_temperature"].mean()
)

fig2 = px.line(
    year_temp,
    x="year",
    y="global_avg_temperature",
    markers=True,
    title="Global Average Temperature Over Years",
    color_discrete_sequence=["#228B22"]
)

fig2.update_traces(texttemplate="%.2f", textposition="top center")
fig2.update_layout(
    template=plot_template,
    title_x=0.5,
    xaxis_title="Year",
    yaxis_title="Average Global Temperature",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    height=550
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
###  📌 Key Insights
- Shows the trend of global average temperature across different years.
- Helps identify periods of increasing or decreasing temperature.
- Useful for understanding long-term climate change patterns.
- Enables comparison of temperature variations over time.
- Supports climate research and environmental policy development.
""")
st.divider()

#---------------------------------------
# GRAPH 3 : SCATTER PLOT
#---------------------------------------

st.subheader("Scatter Plot Representation of CO₂ Concentration vs Temperature Anomaly")
co2_temp = filtered_df[["co2_concentration_ppm", "temperature_anomaly"]]

fig3 = px.scatter(
    co2_temp,
        x="co2_concentration_ppm",
        y="temperature_anomaly",
        color="temperature_anomaly",
        color_continuous_scale="Greens",
        hover_data={
            "co2_concentration_ppm": True,
            "temperature_anomaly": True
        },
        title="Carbon Concentration as compared to Temperature Anomaly",
        size="co2_concentration_ppm",
)
 


fig3.update_traces(texttemplate="%.2f", textposition="top center")
fig3.update_layout(
    template=plot_template,
    title_x=0.5,
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    height=600
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
### 📑Key Insights
- Illustrates the relationship between CO₂ concentration and temperature anomaly.
- Helps identify the impact of greenhouse gas emissions on global temperature changes.
- Supports the analysis of climate change and environmental sustainability.
- Provides valuable information for policymakers and environmental researchers.
- Enables the identification of regions with higher CO₂ emissions and their corresponding temperature anomalies.
""")

st.divider()

#---------------------------------------------------
# GRAPH 4 : PIE CHART
#---------------------------------------------------

st.subheader("Pie Chart Representation of Climate Risk Index Distribution Across Different Countries")
risk_index = (
    filtered_df.groupby("country", as_index=False)["climate_risk_index"].mean()
)

fig4 = px.pie(
    risk_index,
    names="country",
    values="climate_risk_index",
    color="country",
    hole=0.45,
    title="Climate Risk Index Distribution by Country",
   color_discrete_sequence=[
    "#0B3D0B",
    "#145214",
    "#1B5E20",
    "#2E7D32",
    "#388E3C",
    "#43A047",
    "#4CAF50",
    "#66BB6A",
    "#81C784",
    "#A5D6A7"
]
)
fig4.add_annotation(
    text="🌍",
    x=0.5,
    y=0.5,
    font=dict(size=36),
    showarrow=False
)

fig4.update_traces(textinfo="label+value",
                   textfont_size=15,
                   pull=[0.03]*len(risk_index))
fig4.update_layout(
    template=plot_template,
    title=dict(
            text="<b>🌍 Climate Risk Index Distribution</b>",
            x=0.5,
            font=dict(size=24)
    ),
    font=dict(
        family="Arial",
        size=14,
        color="white"
    ),
    legend=dict(
        orientation="h",
        y=-0.15,
        x=0.5,
        xanchor="center"
    ),
    margin=dict(
        t=70,
        b=70,
        l=20,
        r=20
    ),
    height=650
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
### 📜 Key Insights
- Shows the distribution of climate risk indices across different countries.
- Helps identify regions with higher or lower climate risks.
- Supports informed decision-making for climate adaptation and mitigation strategies.
- Provides a visual representation of the varying levels of climate vulnerability.
- Enables policymakers and researchers to prioritize areas for climate action and resource allocation.
""")

st.divider()

#---------------------------------------------------
# GRAPH 5 : BOX PLOT
#---------------------------------------------------

st.subheader("Box Plot Representation of Annual Rainfall Across Different Countries")
rainfall_data = filtered_df[["country", "annual_rainfall_mm"]]

fig5 = px.box(
    rainfall_data,
    x="country",
    y="annual_rainfall_mm",
    title="Annual Rainfall Distribution by Country",
    color="country",
    color_discrete_sequence=[
            "#0B6623",
            "#228B22",
            "#2E8B57",
            "#3CB371",
            "#66CDAA",
            "#90EE90",
        ],
)

fig5.update_traces(quartilemethod="inclusive")
fig5.update_layout(
    template=plot_template,
    title_x=0.5,
    xaxis_title="Country",
    yaxis_title="Annual Rainfall (mm)",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    height=600
)       

st.plotly_chart(fig5, use_container_width=True) 
st.markdown("""
### 📌 Key Insights
- Displays the distribution of annual rainfall across different countries.
- Helps identify regions with higher or lower rainfall patterns.        
- Supports the analysis of climate variability and water resource management.
- Provides insights into potential drought or flood-prone areas.    
- Enables policymakers and researchers to plan for climate adaptation and mitigation strategies.
""")

st.divider()

#---------------------------------------------------
# GRAPH 6 : VIOLIN PLOT
#---------------------------------------------------

st.subheader("Violin Plot Representation of Sea Level Rise Across Different Countries")
sea_level_data= filtered_df[["country", "sea_level_rise_mm"]]

fig6 = px.violin(
    sea_level_data,
    x="country",
    y="sea_level_rise_mm",
    title="Sea Level Rise Distribution by Country",
    color="country",
    box=True,
    color_discrete_sequence=[
        "#0B6623",
        "#228B22",
        "#2E8B57",
        "#3CB371",
        "#66CDAA",
        "#90EE90",
    ],
    points="all"
)   

fig6.update_layout(
    template=plot_template,
    title=dict(
        text="<b>Sea Level Rise Distribution by Country (Violin Plot)</b>",
        x=0.5,
        xanchor="center",
        font=dict(size=24)
    ),
    font=dict(
        family="Arial",
        size=14,
        color="white"
    ),
    xaxis=dict(
        title="Country",
        showgrid=False,
        tickangle=-20
    ),
    yaxis=dict(
        title="Sea Level Rise (mm)",
        showgrid=False,
        zeroline=True
    ),
    legend_title="Country",
    margin=dict(t=70, l=60, r=30, b=60),
    height=650
)

st.plotly_chart(fig6, use_container_width=True)
st.markdown("""
### ☁️ Key Insights
- Illustrates the distribution of sea level rise across different countries.
- Helps identify regions experiencing higher or lower sea level rise.
- Supports the analysis of climate change impacts on coastal areas.
- Provides insights into potential risks of flooding and coastal erosion.
- Enables policymakers and researchers to plan for climate adaptation and mitigation strategies.
""")

st.divider()

#---------------------------------------------------
# GRAPH 7 : BUBBLE CHART
#---------------------------------------------------

st.subheader("Bubble Chart: CO₂ Concentration vs Temperature Anomaly")
energy_data = filtered_df.copy()

# Bubble size must be positive
energy_data["bubble_size"] = energy_data["annual_rainfall_mm"].abs()

fig7 = px.scatter_3d(
    energy_data,
    x="co2_concentration_ppm",
    y="temperature_anomaly",
    z="sea_level_rise_mm",
    size="bubble_size",
    color="country",
    color_discrete_sequence=[
            "#0B6623",
            "#228B22",
            "#2E8B57",
            "#3CB371",
            "#66CDAA",
            "#90EE90",
        ],
    hover_name="country",
    title="3D Climate Analysis"
)

fig7.update_layout(
    template=plot_template,
    title_x=0.5,
    scene=dict(
        xaxis_title="CO₂ Concentration (ppm)",
        yaxis_title="Temperature Anomaly (°C)",
        zaxis_title="Sea Level Rise (mm)"
    ),
    height=700,
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
)

st.plotly_chart(fig7, use_container_width=True)
st.markdown(""" 
### 🌡️ Key Insights
- Shows the relationship between CO₂ concentration, temperature anomaly, and sea level rise.
- Helps identify the impact of greenhouse gas emissions on global temperature changes and sea level rise.
- Supports the analysis of climate change and environmental sustainability. 
- Provides valuable information for policymakers and environmental researchers.
- Enables the identification of regions with higher CO₂ emissions, temperature anomalies, and sea level rise.
""")

st.divider()

#---------------------------------------------------
# GRAPH 8 : CHOROPLETH MAP
#---------------------------------------------------

st.subheader("Choropleth Map: Global Average Temperature by Country")
temp_range = (
    filtered_df.groupby("country", as_index=False)["global_avg_temperature"].mean()
)   

fig8 = px.choropleth(
    temp_range,
    locations="country",
    locationmode="country names",
    color="global_avg_temperature",
    color_continuous_scale="Greens",
    title="Global Average Temperature by Country"
)

fig8.update_layout(
    template=plot_template,
    title_x=0.5,
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type="equirectangular"
    ),
    height=600
)

st.plotly_chart(fig8, use_container_width=True)
st.markdown("""
### 🌍 Key Insights
- Displays the global average temperature distribution across different countries.
- Helps identify regions experiencing higher or lower temperatures.
- Supports the analysis of global climate variations and trends.
- Provides valuable information for environmental monitoring and sustainability studies.
- Enables policymakers and researchers to understand climate change impacts across countries.
""")

st.divider()

#---------------------------------------------------
# GRAPH 9: TREEMAP
#---------------------------------------------------

st.subheader("Tree Map For Climate Risk Index Across Different Countries")
renew_energy = filtered_df.groupby("country", as_index=False)[["climate_risk_index"]].mean()



fig9 = px.treemap(
    renew_energy,
    path=["country"],
    values="climate_risk_index",
    color="climate_risk_index",
    color_continuous_scale=[
        "#0B6623",
        "#228B22",
        "#2E8B57",
        "#3CB371",
        "#66CDAA",
    ],
    title="Climate Risk Index Across Different Countries"
)
fig9.update_traces(
    textinfo="label+value",
    textfont_size=16,
    marker=dict(
        line=dict(color="white", width=2)
    ),
    hovertemplate=
    "<b>%{label}</b><br>"
    "Climate Risk Index: %{value:.2f}<extra></extra>"
)
fig9.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    title=dict(
        text="<b>🌍 Climate Risk Index by Country</b>",
        x=0.5,
        font=dict(size=24)
    ),
    font=dict(
        family="Arial",
        color="white"
    ),
    coloraxis_colorbar=dict(
        title="Risk Index",
        thickness=15
    ),
    margin=dict(t=70,l=15,r=15,b=15),
    height=650
)


st.plotly_chart(fig9, use_container_width=True)

st.markdown("""
### 🌍 Key Insights
- Displays the climate risk index distribution across different countries in a hierarchical format.
- Helps identify regions with higher or lower climate risks.
- Supports informed decision-making for climate adaptation and mitigation strategies.
- Provides a visual representation of the varying levels of climate vulnerability.
- Enables policymakers and researchers to prioritize areas for climate action and resource allocation.
""")

st.divider()

#----------------------------------------
# GRAPH 10: AREA CHART
#----------------------------------------

st.subheader("Area Chart: Yearly Temperature Trends")
rainfall_area = filtered_df.groupby("year", as_index=False)[["annual_rainfall_mm"]].mean()

fig10 = px.area(
    rainfall_area,
    x="year",
    y="annual_rainfall_mm",
    title="Annual Rainfall Trends Over Years",
    color_discrete_sequence=["#0E9E51"]
)

fig10.update_traces(
    line=dict(width=3),
    hovertemplate="<b>Year:</b> %{x}<br>" +
                  "<b>Annual Rainfall:</b> %{y:,.0f} mm<extra></extra>"
)

fig10.update_layout(
    template=plot_template,
    title=dict(
        text="<b>Annual Rainfall Trends Over Years</b>",
        x=0.5,
        xanchor="center",
        font=dict(size=24)
    ),
    font=dict(
        family="Arial",
        size=14,
        color="white"
    ),
    xaxis=dict(
        title="Year",
        tickangle=-45,
        showgrid=False,
        showline=True,
        linecolor="white"
    ),
    yaxis=dict(
        title="Annual Rainfall (mm)",
        showgrid=True,
        gridcolor="rgba(255,255,255,0.15)",
        zeroline=False,
        showline=True,
        linecolor="white"
    ),
    margin=dict(
        t=70,
        l=70,
        r=40,
        b=60
    ),
    height=650,
    showlegend=False
)

st.plotly_chart(fig10, use_container_width=True)

st.markdown("""
### 🌍 Key Insights
- Shows the trend of the annual rainfall over different years.
- Highlights periods of increasing or decreasing values.
- Helps identify long-term climate patterns.
- Supports climate research and environmental monitoring.
- Enables better understanding of how environmental conditions change over time.
""")

st.divider()

#------------------------------------------------
# CLIMATE HEALTH SCORE
#------------------------------------------------
st.subheader("🌍 Climate Health Score")

score = max(0, 100 - filtered_df["climate_risk_index"].mean())

st.progress(int(score))

st.metric("Climate Health", f"{score:.0f}/100")

st.subheader("💡 Recommendations")

risk = filtered_df["climate_risk_index"].mean()

if risk >= 70:
    st.error("""
⚠ High Climate Risk

• Reduce CO₂ emissions
• Increase forest cover
• Promote renewable energy
""")

elif risk >= 40:
    st.warning("""
⚠ Moderate Climate Risk

• Improve water conservation
• Reduce pollution
• Encourage sustainable practices
""")

else:
    st.success("""
✅ Low Climate Risk

• Continue environmental protection
• Maintain green initiatives
""")

#---------------------------------------------------
# FOR ENVIRONMENTAL ORGANIZATIONS
#---------------------------------------------------
with st.expander("🌿 For Environmental Organizations"):

    st.markdown("""
### 🌱 Environmental Recommendations

**1. Carbon Emission Reduction**
- Encourage the adoption of renewable energy sources.
- Promote electric vehicles and sustainable transportation.
- Implement stricter industrial emission standards.

**2. Forest Conservation**
- Increase afforestation and reforestation programs.
- Protect existing forests from deforestation.
- Encourage community-based plantation initiatives.

**3. Water Resource Management**
- Improve rainwater harvesting systems.
- Reduce water wastage through sustainable practices.
- Protect rivers and wetlands from pollution.

**4. Climate Awareness**
- Conduct awareness campaigns about climate change.
- Promote sustainable lifestyles.
- Encourage recycling and waste reduction.
""")

#---------------------------------------------------
# FOR GOVERNMENT & POLICY MAKERS
#---------------------------------------------------

with st.expander("🏛️ For Government & Policy Makers"):

    st.markdown("""
### 📋 Policy Recommendations

- Invest in renewable energy infrastructure.
- Strengthen climate adaptation policies.
- Monitor regions with higher climate risk.
- Encourage sustainable urban planning.
- Promote carbon-neutral industrial practices.
- Increase funding for environmental research.
""")

#-----------------------------------------------
# FOR CLIMATE RESEARCHERS
#-----------------------------------------------

with st.expander("🔬 For Climate Researchers"):

    st.markdown("""
### 📊 Research Insights

#### 🌡 Temperature Trends

- Temperature shows noticeable variations across countries.
- Long-term monitoring helps identify climate change patterns.

#### 🌱 CO₂ Analysis

- Higher CO₂ concentration is associated with increasing temperature anomalies.
- Greenhouse gas monitoring remains essential.

#### 🌊 Sea Level Rise

- Coastal regions require continuous monitoring.
- Rising sea levels indicate long-term environmental changes.

#### 🌧 Rainfall Analysis

- Rainfall patterns differ significantly across countries.
- Seasonal variations influence water availability.
""")

    st.markdown("---")

with st.expander("📌 Climate Cloud Dashboard Summary"):

    st.markdown("""
### 🌍 About Climate Cloud

Climate Cloud is an interactive climate analytics dashboard designed to visualize and analyze key environmental indicators including:

- 🌡️ Global Average Temperature
- 🌱 CO₂ Concentration
- 🌧️ Annual Rainfall
- 🌊 Sea Level Rise
- ⚠️ Climate Risk Index

### ✨ Key Features

- 📊 11 Interactive Visualizations
- 🎯 Dynamic Filters
- 📈 KPI Cards
- 💡 Climate Insights
- 📥 Dataset Download
- 🌍 User-Friendly Dashboard

This dashboard enables users to explore climate trends, compare environmental indicators, and gain meaningful insights for climate awareness and sustainable decision-making.
""")

#----------------RECCOMENDATIONS----------------------------
st.subheader("💡 Recommendations")

st.success("""
✅ Increase Renewable Energy Usage

✅ Reduce Greenhouse Gas Emissions

✅ Protect Forest Ecosystems

✅ Improve Water Conservation

✅ Encourage Sustainable Development

✅ Strengthen Climate Monitoring Systems
""")

#---------------FUTURE SCOPE----------------------------
with st.expander("🚀 Future Scope"):

    st.markdown("""
### Future Enhancements

- 🌍 Live Weather API Integration

- 🤖 Machine Learning Prediction Models

- ☁ Climate Forecasting Dashboard

- 🛰 NASA Satellite Data Integration

- 📈 Real-time Environmental Monitoring

- 🌱 Carbon Footprint Calculator

- 📱 Mobile-Friendly Dashboard

- ☁ Cloud Deployment
""")

#-----------OVERALL CONCLUSION----------------------------

st.markdown("---")

st.header("📌 Project Conclusion & Key Insights")

st.subheader("📊 Climate Data Analysis Summary")

st.markdown("""
Climate Cloud provides an interactive analysis of global climate indicators
including temperature, CO₂ concentration, rainfall, sea level rise,
and climate risk.

Through interactive filters, KPI cards, and multiple visualizations,
the dashboard helps users explore climate patterns across different
countries and years and understand important environmental trends.
""")

st.subheader("🔍 Major Findings & Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
### 🌡️ Temperature & CO₂

- Temperature patterns vary across countries and years.
- CO₂ concentration provides an important indicator of greenhouse gas emissions.
- Temperature anomalies help identify deviations from normal climate conditions.
- Comparing temperature and CO₂ helps understand their relationship.
""")

with col2:
    st.markdown("""
### 🌊 Rainfall & Sea Level

- Annual rainfall varies considerably between regions.
- Changes in rainfall can indicate variations in climate patterns.
- Sea level rise is an important indicator of long-term climate change.
- Coastal regions may face greater environmental challenges.
""")

st.subheader("⚠️ Climate Risk Insights")

st.markdown("""
- Climate risk differs across countries and regions.
- Areas with higher climate risk require greater attention and adaptation planning.
- Multiple environmental indicators should be considered together rather than individually.
- Data-driven analysis can help identify regions that may require stronger climate action.
""")

st.subheader("🚀 Overall Conclusion")

st.success("""
Climate Cloud transforms climate data into meaningful and interactive
visual insights.

The dashboard demonstrates how data analysis can be used to explore
relationships between temperature, CO₂ concentration, rainfall,
sea level rise, and climate risk.

It provides a simple and accessible platform for understanding
climate patterns and supports greater awareness of environmental
challenges and sustainable decision-making.
""")

if st.button("🌍 Tell Me the Climate Story"):

    avg_temp = filtered_df["global_avg_temperature"].mean()
    avg_co2 = filtered_df["co2_concentration_ppm"].mean()
    avg_risk = filtered_df["climate_risk_index"].mean()

    st.success(f"""
### 🌱 Your Climate Story

For the currently selected data:

🌡️ Average temperature: **{avg_temp:.2f} °C**

🌿 Average CO₂ concentration: **{avg_co2:.2f} ppm**

⚠️ Average climate risk: **{avg_risk:.2f}**

These indicators provide a snapshot of the environmental
conditions represented by your selected countries and years.

💡 **Explore the charts above to understand how these
indicators vary and interact across the selected data.**
""")

st.markdown("<hr style='border:2px solid #4A4A4A;'>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;">

<p>
🚀 Built with <b>Python</b> • <b>Pandas</b> • <b>Plotly</b> • <b>Streamlit</b>
</p>

<h5>
Designed by Tanisha
</h5>
<p style="font-size:13px; color:#808080;">
© 2026 All Rights Reserved
</p>

</div>
""", unsafe_allow_html=True)

