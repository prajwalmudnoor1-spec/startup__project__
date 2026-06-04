import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Market Analytics",
    page_icon="📈",
    layout="wide"
)

# -----------------------------------
# Custom Styling
# -----------------------------------

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

# -----------------------------------
# Load Data
# -----------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "startup_data.csv"
    )

    return df

df = load_data()

st.title("📈 Market Analytics Dashboard")

st.write(
    "Analyze market trends, industry distribution, and startup ecosystem patterns"
)

# -----------------------------------
# Sidebar Filters
# -----------------------------------

st.sidebar.header(
    "Market Filters"
)

industry_filter = st.sidebar.multiselect(
    "Industry",
    options=df["Industry"].unique(),
    default=df["Industry"].unique()
)

region_filter = st.sidebar.multiselect(
    "Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry_filter))
    &
    (df["Region"].isin(region_filter))
]

# -----------------------------------
# KPI Metrics
# -----------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Markets",
    filtered_df["Region"].nunique()
)

c2.metric(
    "Industries",
    filtered_df["Industry"].nunique()
)

c3.metric(
    "Total Startups",
    len(filtered_df)
)

c4.metric(
    "Avg Employees",
    round(
        filtered_df["Employees"].mean(),
        0
    )
)

st.divider()

# -----------------------------------
# Industry Market Share
# -----------------------------------

st.subheader(
    "Industry Market Share"
)

industry_count = filtered_df.groupby(
    "Industry"
).size().reset_index(
    name="Count"
)

fig1 = px.pie(
    industry_count,
    names="Industry",
    values="Count",
    title="Industry Share Distribution"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# -----------------------------------
# Regional Startup Distribution
# -----------------------------------

region_count = filtered_df.groupby(
    "Region"
).size().reset_index(
    name="Startups"
)

fig2 = px.bar(
    region_count,
    x="Region",
    y="Startups",
    title="Regional Startup Concentration"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -----------------------------------
# Market Growth Trend
# -----------------------------------

growth = filtered_df.groupby(
    "Year Founded"
).size().reset_index(
    name="Companies"
)

fig3 = px.line(
    growth,
    x="Year Founded",
    y="Companies",
    markers=True,
    title="Market Growth Trend"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# -----------------------------------
# Industry vs Revenue Heatmap
# -----------------------------------

heat = filtered_df.pivot_table(
    values="Revenue (M USD)",
    index="Industry",
    columns="Region",
    aggfunc="mean"
)

fig4 = px.imshow(
    heat,
    aspect="auto",
    title="Industry Revenue Heatmap"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# -----------------------------------
# Employee Distribution
# -----------------------------------

fig5 = px.box(
    filtered_df,
    x="Industry",
    y="Employees",
    title="Employee Distribution by Industry"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# -----------------------------------
# Market Insights
# -----------------------------------

st.subheader(
    "Market Insights"
)

largest_market = region_count.sort_values(
    "Startups",
    ascending=False
).iloc[0]["Region"]

top_industry = industry_count.sort_values(
    "Count",
    ascending=False
).iloc[0]["Industry"]

st.success(
    f"Largest startup market: {largest_market}"
)

st.info(
    f"Dominant industry: {top_industry}"
)

st.warning(
    f"Average company size: {round(filtered_df['Employees'].mean())} employees"
)

# -----------------------------------
# Top Market Players
# -----------------------------------

st.subheader(
    "Top Startups by Market Value"
)

top = filtered_df.sort_values(
    "Valuation (M USD)",
    ascending=False
).head(15)

st.dataframe(
    top,
    use_container_width=True
)

# -----------------------------------
# Dataset Viewer
# -----------------------------------

with st.expander(
    "View Market Dataset"
):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )
