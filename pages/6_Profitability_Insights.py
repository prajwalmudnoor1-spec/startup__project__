import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ------------------------------------
# Page Configuration
# ------------------------------------

st.set_page_config(
    page_title="Profitability Insights",
    page_icon="📈",
    layout="wide"
)

# ------------------------------------
# Styling
# ------------------------------------

st.markdown("""
<style>

.main{
    background-color:#f8fafc;
}

h1,h2,h3{
    color:#1f4e79;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------
# Load Data
# ------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "startup_data.csv"
    )

    return df

df = load_data()

st.title("📈 Profitability Insights Dashboard")

st.write(
    "Analyze profitability performance and business sustainability"
)

# ------------------------------------
# Create Profit Metrics
# ------------------------------------

if "Profit Margin %" not in df.columns:

    df["Profit Margin %"] = (
        (
            df["Revenue (M USD)"]
            -
            df["Funding Amount (M USD)"]
        )
        /
        df["Revenue (M USD)"]
    ) * 100

# ------------------------------------
# Sidebar Filters
# ------------------------------------

st.sidebar.header(
    "Filters"
)

industry = st.sidebar.multiselect(
    "Industry",
    df["Industry"].unique(),
    default=df["Industry"].unique()
)

region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry))
    &
    (df["Region"].isin(region))
]

# ------------------------------------
# KPI Cards
# ------------------------------------

avg_profit = filtered_df[
    "Profit Margin %"
].mean()

max_profit = filtered_df[
    "Profit Margin %"
].max()

profitable_count = (
    filtered_df[
        "Profit Margin %"
    ] > 0
).sum()

profit_ratio = (
    profitable_count
    /
    len(filtered_df)
) * 100

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Avg Profit Margin",
    f"{avg_profit:.2f}%"
)

c2.metric(
    "Highest Margin",
    f"{max_profit:.2f}%"
)

c3.metric(
    "Profitable Startups",
    profitable_count
)

c4.metric(
    "Profitability Rate",
    f"{profit_ratio:.1f}%"
)

st.divider()

# ------------------------------------
# Profit Margin Distribution
# ------------------------------------

fig1 = px.histogram(
    filtered_df,
    x="Profit Margin %",
    nbins=30,
    title="Profit Margin Distribution"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ------------------------------------
# Industry Profitability
# ------------------------------------

industry_profit = filtered_df.groupby(
    "Industry"
)["Profit Margin %"].mean().reset_index()

fig2 = px.bar(
    industry_profit,
    x="Industry",
    y="Profit Margin %",
    title="Average Profit Margin by Industry"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ------------------------------------
# Revenue vs Profitability
# ------------------------------------

fig3 = px.scatter(
    filtered_df,
    x="Revenue (M USD)",
    y="Profit Margin %",
    color="Industry",
    size="Employees",
    hover_name="Startup Name",
    title="Revenue vs Profitability"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ------------------------------------
# Trend Analysis
# ------------------------------------

trend = filtered_df.groupby(
    "Year Founded"
)["Profit Margin %"].mean().reset_index()

fig4 = px.line(
    trend,
    x="Year Founded",
    y="Profit Margin %",
    markers=True,
    title="Profitability Trend"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ------------------------------------
# Top Profitable Companies
# ------------------------------------

st.subheader(
    "Top Profitable Startups"
)

top_profit = filtered_df.sort_values(
    "Profit Margin %",
    ascending=False
).head(10)

st.dataframe(
    top_profit,
    use_container_width=True
)

# ------------------------------------
# Insights
# ------------------------------------

st.subheader(
    "Business Insights"
)

best_industry = industry_profit.sort_values(
    "Profit Margin %",
    ascending=False
).iloc[0]["Industry"]

top_company = top_profit.iloc[0][
    "Startup Name"
]

st.success(
    f"Highest profit industry: {best_industry}"
)

st.info(
    f"Top profitable startup: {top_company}"
)

st.warning(
    f"{profit_ratio:.1f}% startups are profitable"
)

# ------------------------------------
# Dataset Viewer
# ------------------------------------

with st.expander(
    "View Profitability Dataset"
):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )
