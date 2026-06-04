import streamlit as st
import pandas as pd

# -------------------------------
# Page Config
# -------------------------------

st.set_page_config(
    page_title="Startup Analytics Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Styling
# -------------------------------

st.markdown("""
<style>

.main{
    background-color:#f7f9fc;
}

.big-font{
    font-size:40px;
    font-weight:bold;
    color:#1f4e79;
}

.small-text{
    color:gray;
    font-size:18px;
}

.card{
    padding:20px;
    border-radius:10px;
    background:white;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# Load Dataset
# -------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "startup_data.csv"
    )

    return df

df = load_data()

# -------------------------------
# Header
# -------------------------------

st.markdown(
    "<p class='big-font'>🚀 Startup Analytics Dashboard</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='small-text'>Deep Analytics • AI Insights • Business Intelligence</p>",
    unsafe_allow_html=True
)

st.divider()

# -------------------------------
# Sidebar
# -------------------------------

st.sidebar.title(
    "Navigation"
)

st.sidebar.success(
    "Select analytics pages below"
)

st.sidebar.markdown("""
### Available Pages

📊 Executive Dashboard  
💰 Funding Analytics  
💎 Valuation Analytics  
📈 Revenue Analytics  
🌍 Market Analytics  
📉 Profitability Insights  
🤖 AI Insights  
""")

# -------------------------------
# Main KPI Section
# -------------------------------

total_startups = len(df)

total_funding = df[
    "Funding Amount (M USD)"
].sum()

avg_revenue = df[
    "Revenue (M USD)"
].mean()

avg_valuation = df[
    "Valuation (M USD)"
].mean()

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Total Startups",
    total_startups
)

c2.metric(
    "Total Funding",
    f"${total_funding:.2f} M"
)

c3.metric(
    "Average Revenue",
    f"${avg_revenue:.2f} M"
)

c4.metric(
    "Average Valuation",
    f"${avg_valuation:.2f} M"
)

st.divider()

# -------------------------------
# Dataset Preview
# -------------------------------

st.subheader(
    "Dataset Preview"
)

st.dataframe(
    df.head(15),
    use_container_width=True
)

# -------------------------------
# Dataset Information
# -------------------------------

left,right = st.columns(2)

with left:

    st.subheader(
        "Dataset Information"
    )

    st.write(
        f"Rows : {df.shape[0]}"
    )

    st.write(
        f"Columns : {df.shape[1]}"
    )

    st.write(
        "Missing Values:",
        df.isnull().sum().sum()
    )

with right:

    st.subheader(
        "Available Analytics"
    )

    st.write(
        "• Funding Analysis"
    )

    st.write(
        "• Valuation Analytics"
    )

    st.write(
        "• Revenue Analytics"
    )

    st.write(
        "• AI Insights"
    )

    st.write(
        "• Market Analysis"
    )

st.divider()

# -------------------------------
# Quick Insights
# -------------------------------

st.subheader(
    "Quick Insights"
)

top_industry = df.groupby(
    "Industry"
)["Revenue (M USD)"].mean().idxmax()

top_region = df[
    "Region"
].mode()[0]

top_company = df.loc[
    df[
        "Valuation (M USD)"
    ].idxmax(),
    "Startup Name"
]

st.success(
    f"Highest Revenue Industry: {top_industry}"
)

st.info(
    f"Most Active Region: {top_region}"
)

st.warning(
    f"Highest Valuation Startup: {top_company}"
)

st.divider()

# -------------------------------
# Footer
# -------------------------------

st.caption(
    "Startup Analytics Dashboard | Streamlit + Python + Plotly"
)
