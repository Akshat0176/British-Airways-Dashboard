import streamlit as st 
import plotly.express as px 
import pandas as pd 
import numpy as np
import warnings
from PIL import Image
warnings.filterwarnings('ignore') 

# --- Streamlit Configuration (REDUCED VERTICAL SPACE) ---
st.set_page_config(layout = 'wide')
# Reduced top/bottom padding for the main block container and headers
st.markdown('<style>div.block-container{padding-top:1rem; padding-bottom:1rem;}</style>', unsafe_allow_html=True)
st.markdown('<style>h1, h2, h3, h4{margin-top: 0.5rem; margin-bottom: 0.5rem;}</style>', unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data(): 
    df = pd.read_csv('customer_booking.csv', encoding='latin1')    
    df['booking_status'] = df['booking_complete'].map({0: 'Incomplete', 1: 'Complete'})
    df['has_baggage'] = df['wants_extra_baggage'].map({0: 'No', 1: 'Yes'})
    df['has_preferred_seat'] = df['wants_preferred_seat'].map({0: 'No', 1: 'Yes'})
    df['has_in_flight_meals'] = df['wants_in_flight_meals'].map({0: 'No', 1: 'Yes'})
    day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    df['flight_day'] = pd.Categorical(df['flight_day'], categories=day_order, ordered=True)
    df = df[df['purchase_lead'] >= 0]
    df = df[df['length_of_stay'] >= 0]
    return df
data_load_state = st.text('Loading data...')
df = load_data()
data_load_state.text("Data loaded successfully! (using st.cache_data)") 

# --- Header (Logo and Title - COMPACTED) ---

# Try to load images once
images_loaded = False
try:
    # Ensure this file exists in your directory
    logo_image = Image.open("britishairwayslogo5.png")  
    # Ensure this file exists in your directory
    airbus_image = Image.open('airbus Background Removed.png')
    images_loaded = True 
except FileNotFoundError:
    st.warning("Image files not found! Displaying dashboard structure without them.")

# Use smaller ratio for images
col1, col2, col3 = st.columns([1, 8, 1])

with col1:
    if images_loaded:
        st.image(logo_image, width=200) # Reduced width

with col2:
    html_title_centered = """
    <style>
    .centered-title-text {
        font-weight: bold;
        padding: 0px; /* Reduced padding */
        text-align: center; 
        margin-top: 0; 
        margin-bottom: 0;
    }
    </style>
    <h1 class="centered-title-text">British Airways Dashboard ✈️</h1>
    """
    st.markdown(html_title_centered, unsafe_allow_html=True)

with col3:
    if images_loaded:
        st.image(airbus_image, width=100) # Reduced width

st.header("✈️ British Airways Overview")

# --- Core Metrics (CONDENSED) ---
# Calculations
longest_flight_duration = df['flight_duration'].max()
shortest_flight_duration = df['flight_duration'].min()
longest_route = df.loc[df['flight_duration'].idxmax(), 'route']
shortest_route = df.loc[df['flight_duration'].idxmin(), 'route']
completion_rate = df['booking_complete'].mean() * 100
most_travelled_route = df['route'].value_counts().idxmax()
total_bookings = len(df)

col_a, col_b, col_c, col_d, col_e = st.columns(5)

with col_a:
    st.metric(label="Total Bookings", value=f"{total_bookings:,}")
with col_b:
    st.metric(label="Completion Rate", value=f"{completion_rate:.2f} %") 
with col_c: 
    st.metric(label="Most Travelled Route", value=f"{most_travelled_route}")
with col_d:
    st.metric(label="Longest Flight (hrs)", value=f"{longest_flight_duration}", delta=f"{longest_route}")
with col_e:
    st.metric(label="Shortest Flight (hrs)", value=f"{shortest_flight_duration}", delta=f"{shortest_route}")

# Soft gray divider line
st.markdown(
    """
    <hr style="border: 0.5px solid #888888; opacity: 0.5; margin-top: 0.5rem; margin-bottom: 0.5rem;">
    """,
    unsafe_allow_html=True
) 

# --- Geographical and Route Analysis (SIDE-BY-SIDE) ---
col_map, col_route = st.columns([2, 1])

with col_map:
    st.subheader("Bookings by Originating Country")
    map_df = df['booking_origin'].value_counts().reset_index()
    map_df.columns = ['booking_origin', 'Total_Bookings']
    fig_map = px.choropleth(
        map_df, locations="booking_origin", locationmode='country names', 
        color="Total_Bookings", hover_name="booking_origin",
        color_continuous_scale=px.colors.sequential.Plasma,
        title='Total Bookings by Originating Country', template="streamlit"
    )
    fig_map.update_geos(showcountries=True, countrycolor="Gray", showocean=True, oceancolor="lightblue")
    fig_map.update_layout(
        height=400, # Reduced height
        margin={"r":0, "t":40, "l":0, "b":0}, coloraxis_colorbar_title="Bookings"
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col_route:
    st.subheader('Flight Routes Overview')
    st.markdown("##### Top Route Counts")
    route_counts = df['route'].value_counts().head(10) # Showing top 10 for better fit
    st.bar_chart(route_counts, height=360) # Matched map height


# --- Multi-Plot Analysis (THREE COLUMNS - Heatmap Replaced) ---

col1, col2, col3 = st.columns([1, 1, 1])
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

with col1:
    st.subheader('Distribution of Bookings')
    st.markdown("##### Origin Breakdown")
    booking_counts = df['booking_origin'].value_counts().reset_index()
    booking_counts.columns = ['booking_origin', 'Total_Bookings']
    fig = px.pie(
        booking_counts.head(10), # Show top 10 for clarity and compactness
        values='Total_Bookings', names='booking_origin',
        color_discrete_sequence=px.colors.sequential.Plasma,
        
    )
    fig.update_traces(textposition='inside', textinfo='percent') # Removed label for compactness
    fig.update_layout(showlegend=True, height=350, margin=dict(t=30, b=0, l=0, r=0)) # Reduced height
    st.plotly_chart(fig, use_container_width=True)

with col2: 
    st.subheader('Scatter Plots: Relationship Finder')
    st.markdown("##### Select Axes:")
    
    col_x, col_y = st.columns(2)

    purchase_lead_idx = numeric_cols.index('purchase_lead') if 'purchase_lead' in numeric_cols else 0
    length_of_stay_idx = numeric_cols.index('length_of_stay') if 'length_of_stay' in numeric_cols else (1 if len(numeric_cols) > 1 else 0)

    with col_x:
        selected_col_x = st.selectbox("X-axis:", numeric_cols, index=purchase_lead_idx, key='scatter_x')
    with col_y:
        selected_col_y = st.selectbox("Y-axis:", numeric_cols, index=length_of_stay_idx, key='scatter_y')

    fig_scatter = px.scatter(
        df, x=selected_col_x, y=selected_col_y,
        color='booking_status', 
        color_discrete_map={'Complete': '#0072B2', 'Incomplete': '#D55E00'}, 
        opacity=0.6,
        title=f"{selected_col_x} vs {selected_col_y}",
        template="plotly_white",
        height=350, # Reduced height
        hover_data=['route', 'booking_origin']
    )
    fig_scatter.update_layout(xaxis_title=selected_col_x, yaxis_title=selected_col_y, legend_title="Status")
    st.plotly_chart(fig_scatter, use_container_width=True)
    
# --- REPLACEMENT FOR HEATMAP: DAY/TIME ANALYSIS ---
with col3:
    st.subheader('Day/Time Analysis')
    st.markdown("##### Bookings Count by Flight Day")
    
    day_counts = df['flight_day'].value_counts().sort_index().reset_index()
    day_counts.columns = ['flight_day', 'Total_Bookings']

    fig_day = px.bar(
        day_counts,
        x='flight_day', y='Total_Bookings',
        color='flight_day',
        color_discrete_sequence=px.colors.qualitative.T10,
        title='Bookings by Day of the Week',
        template='plotly_white',
        height=350 # Matched height of other plots in this row
    )
    fig_day.update_layout(xaxis_title="Flight Day", yaxis_title="Total Bookings", showlegend=False)
    st.plotly_chart(fig_day, use_container_width=True)


# --- Distribution and Outlier Analysis (SIDE-BY-SIDE) ---
st.markdown(
    """
    <hr style="border: 0.5px solid #888888; opacity: 0.5; margin-top: 0.5rem; margin-bottom: 0.5rem;">
    """,
    unsafe_allow_html=True
) 

col_hist, col_box = st.columns(2) # Reduced to two columns

with col_hist:
    st.subheader("Distribution Analysis")
    st.markdown("##### Histogram of Selected Entity")
    selected_col_hist = st.selectbox(
        "Select distribution variable:", 
        numeric_cols, 
        index=numeric_cols.index('purchase_lead') if 'purchase_lead' in numeric_cols else 0,
        key='hist_final_select'
    )
    
    fig_hist = px.histogram(
        df, x=selected_col_hist, nbins=30,
        title=f"Distribution of {selected_col_hist}",
        template="plotly_white", color_discrete_sequence=['#0072B2'],
        height=350 
    )
    fig_hist.update_layout(xaxis_title=selected_col_hist, yaxis_title="Frequency", bargap=0.1)
    st.plotly_chart(fig_hist, use_container_width=True)

with col_box:
    st.subheader("Outlier Analysis")
    st.markdown("##### Box Plot by Booking Status")
    # Box Plot 
    selected_box_col = st.selectbox("Select variable for box plot:", numeric_cols, key='box_final_select')

    fig_box = px.box(
        df, y=selected_box_col, color='booking_status',
        color_discrete_map={'Complete': '#0072B2', 'Incomplete': '#D55E00'},
        title=f"Box Plot of {selected_box_col}",
        template="plotly_white",
        height=350 
    )
    fig_box.update_layout(yaxis_title=selected_box_col, xaxis_title="Booking Status", showlegend=True)
    st.plotly_chart(fig_box, use_container_width=True)