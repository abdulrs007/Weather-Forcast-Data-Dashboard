import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import time
from backend import get_data

# Configure page
st.set_page_config(
    page_title="Weather Forecast Pro",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }

    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #fff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    .main-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        font-weight: 300;
        margin-bottom: 0;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    .sidebar .stSelectbox label, .sidebar .stTextInput label, .sidebar .stSlider label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }

    /* Input field styling */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.2) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.7) !important;
    }

    .stSelectbox > div > div > select {
        background: rgba(255,255,255,0.2) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(238, 90, 36, 0.4) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 35px rgba(238, 90, 36, 0.6) !important;
    }

    /* Metric cards */
    .css-1r6slb0 {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 15px !important;
        padding: 1rem !important;
    }

    /* Content containers */
    .weather-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
    }

    /* Success/Error messages */
    .stAlert {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }

    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24) !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Weather icon animations */
    .weather-icon {
        font-size: 4rem;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    /* Chart container */
    .chart-container {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 1rem;
        backdrop-filter: blur(10px);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🌤️ Weather Forecast Pro</h1>
    <p class="main-subtitle">Advanced weather insights with stunning visualizations</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for controls
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")

    # Location input with enhanced styling
    place = st.text_input(
        "🌍 Enter Location",
        placeholder="e.g., New York, London, Tokyo...",
        help="Enter any city name to get weather forecast"
    )

    # Days slider with custom styling
    days = st.slider(
        "📅 Forecast Duration",
        min_value=1,
        max_value=5,
        value=3,
        help="Select number of days for weather forecast"
    )

    # Data type selection
    option = st.selectbox(
        "📊 Data Visualization",
        ("Temperature", "Sky", "Detailed Analysis"),
        help="Choose what weather data to display"
    )

    # Additional controls
    st.markdown("---")
    st.markdown("### ⚙️ Display Options")

    show_metrics = st.checkbox("Show Key Metrics", value=True)
    animate_charts = st.checkbox("Animated Charts", value=True)

    # Quick location buttons
    st.markdown("### 🌏 Quick Locations")
    col1, col2 = st.columns(2)

    quick_locations = ["New York", "London", "Tokyo", "Paris", "Sydney", "Dubai"]

    for i, location in enumerate(quick_locations):
        if i % 2 == 0:
            if col1.button(location, key=f"quick_{i}"):
                st.session_state.quick_location = location
        else:
            if col2.button(location, key=f"quick_{i}"):
                st.session_state.quick_location = location

# Use quick location if selected
if 'quick_location' in st.session_state:
    place = st.session_state.quick_location

# Main content area
if place:
    # Create columns for layout
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <h2 style="color: white; font-weight: 600;">
                {option} forecast for the next {days} {'day' if days == 1 else 'days'} in 
                <span style="color: #ff6b6b;">{place}</span>
            </h2>
        </div>
        """, unsafe_allow_html=True)

    try:
        # Show loading animation
        with st.spinner('🌐 Fetching weather data...'):
            time.sleep(1)  # Simulate loading
            filtered_data = get_data(place, days)

        if not filtered_data:
            st.error("❌ No data available for this location")
            st.stop()

        # Key metrics display
        if show_metrics:
            st.markdown("### 📈 Key Weather Metrics")

            # Calculate metrics
            temperatures = [d["main"]["temp"] / 10 for d in filtered_data]
            avg_temp = sum(temperatures) / len(temperatures)
            max_temp = max(temperatures)
            min_temp = min(temperatures)

            # Weather conditions summary
            conditions = [d["weather"][0]["main"] for d in filtered_data]
            most_common = max(set(conditions), key=conditions.count)

            # Display metrics in columns
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

            with metric_col1:
                st.metric(
                    label="🌡️ Avg Temperature",
                    value=f"{avg_temp:.1f}°C",
                    delta=f"{avg_temp - 20:.1f}°C from comfort zone"
                )

            with metric_col2:
                st.metric(
                    label="🔥 Max Temperature",
                    value=f"{max_temp:.1f}°C",
                    delta=f"{max_temp - avg_temp:.1f}°C above avg"
                )

            with metric_col3:
                st.metric(
                    label="❄️ Min Temperature",
                    value=f"{min_temp:.1f}°C",
                    delta=f"{min_temp - avg_temp:.1f}°C below avg"
                )

            with metric_col4:
                st.metric(
                    label="🌤️ Dominant Weather",
                    value=most_common,
                    delta="Most frequent condition"
                )

        # Weather visualization based on selected option
        if option == "Temperature":
            st.markdown("### 🌡️ Temperature Trends")

            # Prepare data
            temperatures = [d["main"]["temp"] / 10 for d in filtered_data]
            dates = [d["dt_txt"] for d in filtered_data]

            # Create DataFrame
            df = pd.DataFrame({
                'Date': pd.to_datetime(dates),
                'Temperature': temperatures
            })

            # Create enhanced temperature chart
            fig = go.Figure()

            # Add temperature line
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=df['Temperature'],
                mode='lines+markers',
                name='Temperature',
                line=dict(color='#ff6b6b', width=3, shape='spline'),
                marker=dict(size=8, color='#fff', line=dict(color='#ff6b6b', width=2)),
                fill='tonexty',
                fillcolor='rgba(255, 107, 107, 0.1)'
            ))

            # Add temperature range bands
            fig.add_hline(y=20, line_dash="dash", line_color="rgba(255,255,255,0.5)",
                          annotation_text="Comfort Zone", annotation_position="bottom right")

            # Update layout
            fig.update_layout(
                title=dict(
                    text=f"Temperature Forecast - {place}",
                    font=dict(size=24, color='white', family='Inter'),
                    x=0.5
                ),
                xaxis_title="Date & Time",
                yaxis_title="Temperature (°C)",
                font=dict(color='white', family='Inter'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
                showlegend=False,
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

            # Temperature distribution
            st.markdown("### 📊 Temperature Distribution")

            hist_fig = px.histogram(
                df, x='Temperature', nbins=15,
                title="Temperature Distribution",
                color_discrete_sequence=['#ff6b6b']
            )

            hist_fig.update_layout(
                font=dict(color='white', family='Inter'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                height=400
            )

            st.plotly_chart(hist_fig, use_container_width=True)

        elif option == "Sky":
            st.markdown("### 🌤️ Sky Conditions")

            # Weather icons mapping
            weather_icons = {
                "Clear": "☀️",
                "Clouds": "☁️",
                "Rain": "🌧️",
                "Snow": "❄️",
                "Thunderstorm": "⛈️",
                "Drizzle": "🌦️",
                "Mist": "🌫️"
            }

            # Group data by day
            daily_weather = {}
            for data_point in filtered_data:
                date = data_point["dt_txt"].split()[0]
                condition = data_point["weather"][0]["main"]

                if date not in daily_weather:
                    daily_weather[date] = []
                daily_weather[date].append(condition)

            # Create weather cards
            cols = st.columns(min(len(daily_weather), 5))

            for idx, (date, conditions) in enumerate(daily_weather.items()):
                most_common_condition = max(set(conditions), key=conditions.count)
                icon = weather_icons.get(most_common_condition, "🌤️")

                # Format date
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%a, %b %d")

                with cols[idx % 5]:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%);
                        backdrop-filter: blur(20px);
                        border: 1px solid rgba(255,255,255,0.1);
                        border-radius: 15px;
                        padding: 1.5rem;
                        text-align: center;
                        margin: 0.5rem 0;
                        transition: transform 0.3s ease;
                    ">
                        <div class="weather-icon" style="font-size: 3rem; margin-bottom: 0.5rem;">
                            {icon}
                        </div>
                        <div style="color: white; font-weight: 600; margin-bottom: 0.5rem;">
                            {formatted_date}
                        </div>
                        <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                            {most_common_condition}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Weather conditions pie chart
            st.markdown("### 📊 Weather Conditions Distribution")

            all_conditions = [d["weather"][0]["main"] for d in filtered_data]
            condition_counts = pd.Series(all_conditions).value_counts()

            pie_fig = px.pie(
                values=condition_counts.values,
                names=condition_counts.index,
                title="Weather Conditions Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )

            pie_fig.update_layout(
                font=dict(color='white', family='Inter'),
                paper_bgcolor='rgba(0,0,0,0)',
                height=500
            )

            st.plotly_chart(pie_fig, use_container_width=True)

        elif option == "Detailed Analysis":
            st.markdown("### 📊 Comprehensive Weather Analysis")

            # Prepare comprehensive data
            df = pd.DataFrame({
                'DateTime': pd.to_datetime([d["dt_txt"] for d in filtered_data]),
                'Temperature': [d["main"]["temp"] / 10 for d in filtered_data],
                'Humidity': [d.get("main", {}).get("humidity", 50) for d in filtered_data],
                'Pressure': [d.get("main", {}).get("pressure", 1013) for d in filtered_data],
                'Condition': [d["weather"][0]["main"] for d in filtered_data]
            })

            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Temperature Trend', 'Humidity Levels', 'Atmospheric Pressure', 'Weather Timeline'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )

            # Temperature
            fig.add_trace(
                go.Scatter(x=df['DateTime'], y=df['Temperature'],
                           name='Temperature', line=dict(color='#ff6b6b')),
                row=1, col=1
            )

            # Humidity
            fig.add_trace(
                go.Scatter(x=df['DateTime'], y=df['Humidity'],
                           name='Humidity', line=dict(color='#4ecdc4')),
                row=1, col=2
            )

            # Pressure
            fig.add_trace(
                go.Scatter(x=df['DateTime'], y=df['Pressure'],
                           name='Pressure', line=dict(color='#45b7d1')),
                row=2, col=1
            )

            # Weather conditions as bar chart
            condition_counts = df['Condition'].value_counts()
            fig.add_trace(
                go.Bar(x=condition_counts.index, y=condition_counts.values,
                       name='Conditions', marker_color='#96ceb4'),
                row=2, col=2
            )

            fig.update_layout(
                height=800,
                showlegend=False,
                font=dict(color='white', family='Inter'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

            # Update all subplot backgrounds
            for i in range(1, 3):
                for j in range(1, 3):
                    fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)', row=i, col=j)
                    fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)', row=i, col=j)

            st.plotly_chart(fig, use_container_width=True)

            # Data summary table
            st.markdown("### 📋 Weather Data Summary")

            summary_df = df.groupby(df['DateTime'].dt.date).agg({
                'Temperature': ['mean', 'min', 'max'],
                'Humidity': 'mean',
                'Pressure': 'mean',
                'Condition': lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown'
            }).round(2)

            summary_df.columns = ['Avg Temp (°C)', 'Min Temp (°C)', 'Max Temp (°C)',
                                  'Avg Humidity (%)', 'Avg Pressure (hPa)', 'Dominant Condition']

            st.dataframe(
                summary_df,
                use_container_width=True,
                height=300
            )

    except KeyError as e:
        st.error(f"❌ Location '{place}' not found. Please check the spelling and try again.")
        st.info("💡 **Tip**: Try searching for major cities or include country names for better results.")

        # Suggest popular locations
        st.markdown("### 🌟 Popular Locations to Try:")
        popular_cities = ["New York, USA", "London, UK", "Tokyo, Japan", "Paris, France", "Sydney, Australia"]

        cols = st.columns(len(popular_cities))
        for i, city in enumerate(popular_cities):
            with cols[i]:
                if st.button(city, key=f"popular_{i}"):
                    st.session_state.quick_location = city.split(',')[0]
                    st.experimental_rerun()

    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")
        st.info("🔄 Please try again or contact support if the issue persists.")

else:
    # Welcome screen
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; color: white;">
        <div style="font-size: 6rem; margin-bottom: 2rem;">🌤️</div>
        <h2 style="font-weight: 300; margin-bottom: 1rem; font-size: 2rem;">
            Welcome to Weather Forecast Pro
        </h2>
        <p style="font-size: 1.2rem; opacity: 0.8; margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto;">
            Get detailed weather forecasts with beautiful visualizations. 
            Enter a location in the sidebar to get started with your weather journey.
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-top: 3rem;">
            <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 15px; backdrop-filter: blur(10px);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌡️</div>
                <div style="font-weight: 600;">Temperature Trends</div>
                <div style="opacity: 0.8; font-size: 0.9rem;">Interactive charts & analysis</div>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 15px; backdrop-filter: blur(10px);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌤️</div>
                <div style="font-weight: 600;">Sky Conditions</div>
                <div style="opacity: 0.8; font-size: 0.9rem;">Visual weather patterns</div>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 15px; backdrop-filter: blur(10px);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
                <div style="font-weight: 600;">Detailed Analysis</div>
                <div style="opacity: 0.8; font-size: 0.9rem;">Comprehensive insights</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.6); padding: 1rem;">
    <p>🌤️ Weather Forecast Pro | Built with Streamlit & Plotly | Data powered by your backend API</p>
</div>
""", unsafe_allow_html=True)