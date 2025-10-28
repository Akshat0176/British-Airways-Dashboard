import streamlit as st 
import plotly.express as px 
import pandas as pd 
import numpy as np
import time
from PIL import Image
import warnings
warnings.filterwarnings('ignore') 

# Streamlit Configuration
st.set_page_config(layout = 'wide')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Data Loading
@st.cache_data
def load_data(): 
    df = pd.read_csv('customer_booking.csv', encoding='latin1')    
    df['booking_status'] = df['booking_complete'].map({0: 'Incomplete', 1: 'Complete'})
    df['has_baggage'] = df['wants_extra_baggage'].map({0: 'No', 1: 'Yes'})
    df['has_preferred_seat'] = df['wants_preferred_seat'].map({0: 'No', 1: 'Yes'})
    df['has_in_flight_meals'] = df['wants_in_flight_meals'].map({0: 'No', 1: 'Yes'})
    day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    df['flight_day'] = pd.Categorical(df['flight_day'], categories=day_order, ordered=True)
    # Basic data cleaning: handle outliers in lead time and stay duration
    df = df[df['purchase_lead'] >= 0]
    df = df[df['length_of_stay'] >= 0]
    return df
# --- CRITICAL FIX: Call the function and assign its return value to df ---
data_load_state = st.text('Loading data...')
df = load_data()
data_load_state.text("Data loaded successfully! (using st.cache_data)") 

# Header (Logo and Title)

try:
    # 1. Load the logo (Ensure 'britishairwayslogo5.png' is in the repo)
    logo_image = Image.open("britishairwayslogo5.png")  
    
    # 2. Load the airbus image (Ensure 'airbus Background Removed.png' is in the repo)
    airbus_image = Image.open('airbus Background Removed.png')
    
    # Flag to check if images were loaded successfully
    images_loaded = True 

except FileNotFoundError:
    st.error("Deployment Error: Image files not found! Ensure 'britishairwayslogo5.png' and 'airbus Background Removed.png' are committed to the repository.")
    images_loaded = False

# Using a more appropriate ratio for a logo and a wide title column
col1, col2, col3 = st.columns([2, 8, 1])

with col1:
    if images_loaded:
        st.image(logo_image, width=200)  # smaller width for side column

with col2:
    html_title_centered = """
    <style>
    .centered-title-text {
        font-weight: bold;
        padding: 5px;
        border-radius: 6px;
        text-align: center; 
    }
    </style>
    <h1 class="centered-title-text">British Airways Dashboard</h1>
    """
    st.markdown(html_title_centered, unsafe_allow_html=True)

st.header("✈️ British Airways Overview")

with col3:
    if images_loaded:
        st.image(airbus_image, width=200)


# Core metrics
most_travelled_route = df['route'].value_counts().idxmax()
route_count = df['route'].value_counts().max()

# Find longest and shortest flights
longest_flight_duration = df['flight_duration'].max()
shortest_flight_duration = df['flight_duration'].min()

# Find the corresponding routes
longest_route = df.loc[df['flight_duration'].idxmax(), 'route']
shortest_route = df.loc[df['flight_duration'].idxmin(), 'route']

# Completion rate
completion_rate = df['booking_complete'].mean() * 100

most_travelled_route = df['route'].value_counts().idxmax()

avg_passengers = df['num_passengers'].mean()
# Layout columns
col_a, col_b, col_c, col_d, col_e= st.columns(5)

with col_a:
    st.metric(
        label="Total Bookings",
        value=f"{len(df):,}"
    )

with col_b:
    st.metric(
        label="Longest Flight",
        value=f"{longest_flight_duration} hrs",
        delta=f"{longest_route}"
    )

with col_c:
    st.metric(
        label="Shortest Flight",
        value=f"{shortest_flight_duration} hrs",
        delta=f"{shortest_route}"
    )

with col_d:
    st.metric(
        label="Completion Rate",
        value=f"{completion_rate:.2f} %"
    ) 
with col_e: 
    st.metric( 
        label = "Most Travelled Route",
        value = f"{most_travelled_route}"
    )



st.subheader("Map of Flight Bookings")
map_df = df['booking_origin'].value_counts().reset_index()
map_df.columns = ['booking_origin', 'Total_Bookings']
fig_map = px.choropleth(
    map_df,
    locations="booking_origin",
    locationmode='country names', 
    color="Total_Bookings",
    hover_name="booking_origin",
    color_continuous_scale=px.colors.sequential.Plasma,
    title='Total Bookings by Originating Country',
    template="streamlit"
)

# Customize map appearance
fig_map.update_geos(
    showcoastlines=True,
    coastlinecolor="Black",
    showland=True,
    landcolor="white",
    showocean=True,
    oceancolor="lightblue",
    showcountries=True,
    countrycolor="Black"
)

fig_map.update_layout(
    height=500,
    margin={"r":0, "t":40, "l":0, "b":0},
    coloraxis_colorbar_title="Bookings"
)

st.plotly_chart(fig_map, use_container_width=True)

# Soft gray divider line
st.markdown(
    """
    <hr style="border: 0.5px solid #888888; opacity: 0.5; margin-top: 1rem; margin-bottom: 1rem;">
    """,
    unsafe_allow_html=True
) 
st.subheader('Flight Routes of British Airways')
route_counts = df['route'].value_counts()  
st.bar_chart(route_counts) 
st.subheader("📊 Distribution of Key Numeric Entities")
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
# Let user pick a column to visualize
selected_col = st.selectbox("Select a column to view its distribution:", numeric_cols)
# Plotly histogram
fig_hist = px.histogram(
    df,
    x=selected_col,
    nbins=30,
    title=f"Distribution of {selected_col}",
    template="plotly_white",
    color_discrete_sequence=['#0072B2']
)
fig_hist.update_layout(
    xaxis_title=selected_col,
    yaxis_title="Frequency",
    bargap=0.1,
    height=400
)
st.plotly_chart(fig_hist, use_container_width=True)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.subheader('Distribution of Bookings')
    booking_counts = df['booking_origin'].value_counts().reset_index()
    booking_counts.columns = ['booking_origin', 'Total_Bookings']
    # Plot pie chart
    fig = px.pie(
        booking_counts,
        values='Total_Bookings',
        names='booking_origin',
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with col2: 
    st.subheader('Scatter Plots')
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()


    # 2. Allow user to pick two columns for X and Y axes
    col_x, col_y = st.columns(2)

    with col_x:
        selected_col_x = st.selectbox(
            "Select X-axis variable:",
            numeric_cols,
            index=numeric_cols.index('purchase_lead') if 'purchase_lead' in numeric_cols else 0
        )

    with col_y:
        # Prevent selecting the same column for both, if possible
        default_y_index = numeric_cols.index('length_of_stay') if 'length_of_stay' in numeric_cols else (1 if len(numeric_cols) > 1 else 0)
        selected_col_y = st.selectbox(
            "Select Y-axis variable:",
            numeric_cols,
            index=default_y_index
        )

    # 3. Plotly Scatter Plot
    fig_scatter = px.scatter(
        df,
        x=selected_col_x,
        y=selected_col_y,
        # Color the points by the booking status for better insight
        color='booking_status', 
        color_discrete_map={'Complete': '#0072B2', 'Incomplete': '#D55E00'}, # Adjusted colors
        opacity=0.6,
        title=f"Relationship between {selected_col_x} and {selected_col_y}",
        template="plotly_white",
        height=500,
        hover_data=['route', 'booking_origin'] # Add relevant hover info
    )
    
    # Customize layout and axes
    fig_scatter.update_layout(
        xaxis_title=selected_col_x,
        yaxis_title=selected_col_y,
        legend_title="Booking Status"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)
with col3:
    st.subheader('Feature Correlation Heatmap')
    numeric_df = df.select_dtypes(include=[np.number])  
    corr_matrix = numeric_df.corr(numeric_only=True)
    
    heatmap_fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='Plasma',
        title='Correlation Between Numeric Features'
    )
    heatmap_fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=40, b=0),
        template='simple_white'
    )
    st.plotly_chart(heatmap_fig, use_container_width=True)

st.subheader("Box Plot of Numeric Entities")

# Select only numeric columns
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

# Let user pick a column to visualize
selected_box_col = st.selectbox("Select a column to view its box plot:", numeric_cols)

# Plotly box plot
fig_box = px.box(
    df,
    y=selected_box_col,
    color='booking_status',  # Color by completion status for more insight
    color_discrete_map={'Complete': '#0072B2', 'Incomplete': '#D55E00'},
    title=f"Box Plot of {selected_box_col} by Booking Status",
    template="plotly_white",
    height=400
)

fig_box.update_layout(
    yaxis_title=selected_box_col,
    xaxis_title="Booking Status",
    showlegend=True
)

st.plotly_chart(fig_box, use_container_width=True)


# Plotly histogram
fig_hist = px.histogram(
    df,
    x=selected_col,
    nbins=30,
    title=f"Distribution of {selected_col}",
    template="plotly_white",
    color_discrete_sequence=['#0072B2']
)
fig_hist.update_layout(
    xaxis_title=selected_col,
    yaxis_title="Frequency",
    bargap=0.1,
    height=400
)
st.markdown("### Bookings Count by Flight Day")

# Aggregate data
day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
flight_day_counts = df.groupby('flight_day').size().reset_index(name='Total_Bookings')

# Ensure correct categorical order
flight_day_counts['flight_day'] = pd.Categorical(flight_day_counts['flight_day'], categories=day_order, ordered=True)
flight_day_counts = flight_day_counts.sort_values('flight_day')

# Create Plotly figure
fig_day = px.bar(
    flight_day_counts,
    x='flight_day',
    y='Total_Bookings',
    color='Total_Bookings',
    color_continuous_scale=px.colors.sequential.Teal,
    labels={'Total_Bookings': 'Total Bookings', 'flight_day': 'Flight Day of Week'},
    template="plotly_white"
)
fig_day.update_layout(height=400)  
st.plotly_chart(fig_day)           




























