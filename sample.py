import streamlit as st 
import plotly.express as px 
import pandas as pd 
import warnings
import os
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Superstore!!', page_icon="📊", layout="wide")
st.title("📊 Sample Superstore EDA", width = "stretch")

st.markdown(
    """
    <style>
    div.block-container {
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# File upload
fl = st.file_uploader("📁 Upload a file", type=["csv", "txt", "xlsx", "xls"])

if fl is not None:
    filename = fl.name
    st.write(f"✅ Uploaded file: {filename}")

    if filename.endswith(".csv"):
        df = pd.read_csv(fl)
    elif filename.endswith(".txt"):
        df = pd.read_csv(fl, delimiter="\t")
    else:
        df = pd.read_excel(fl, engine="openpyxl")
else:
    st.write("📂 No file uploaded — loading default dataset...")
    df = pd.read_excel("/Users/akshat17/Desktop/Samplesuperstore.xls", engine="xlrd")

# Date conversion
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

startdate = df["Order Date"].min()
enddate = df["Order Date"].max()

if pd.isnull(startdate) or pd.isnull(enddate):
    startdate, enddate = pd.Timestamp("2015-01-01"), pd.Timestamp("2018-12-31")

st.write(f"📅 Data from {startdate.date()} to {enddate.date()}")

col1, col2 = st.columns(2)
with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startdate))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", enddate))

df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

# Sidebar filters
st.sidebar.header("🎚️ Choose your filter:")

region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

state = st.sidebar.multiselect("Pick the State", df2["State"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

city = st.sidebar.multiselect("Pick the City", df3["City"].unique())
if not city:
    df4 = df3.copy()
else:
    df4 = df3[df3["City"].isin(city)]

st.write("✅ Data filtered successfully!")
st.dataframe(df4.head())





            


