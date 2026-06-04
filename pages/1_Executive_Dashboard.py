import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# Custom Styling
# -------------------------

st.markdown("""
<style>
.main{
    background-color:#f7f9fc;
}

.metric-box{
    background:#ffffff;
    padding:15px;
    border-radius:10px;
}

h1,h2,h3{
    color:#1f4e79;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Load Data
# -------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("startup_data.csv")
    return df

df = load_data()

st.title("📊 Executive Dashboard")
st.write("Startup ecosystem overview and business insights")

# -------------------------
# Sidebar Filters
# -------------------------

st.sidebar.header("Filters")

industry_filter = st.sidebar.multiselect(
    "Select Industry",
    options=df["Industry"].unique(),
    default=df["Industry"].unique()
)

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry_filter))
    &
    (df["Region"].isin(region_filter))
]

# -------------------------
# KPI Cards
# -------------------------

total_startups = len(filtered_df)

total_funding = filtered_df[
    "Funding Amount (M USD)"
].sum()

avg_revenue = filtered_df[
    "Revenue (M USD)"
].mean()

avg_valuation = filtered_df[
    "Valuation (M USD)"
].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Startups",
    total_startups
)

col2.metric(
    "Total Funding",
    f"${total_funding:.1f} M"
)

col3.metric(
    "Average Revenue",
    f"${avg_revenue:.2f} M"
)

col4.metric(
    "Average Valuation",
    f"${avg_valuation:.2f} M"
)

st.divider()

# -------------------------
# Row 1 Charts
# -------------------------

left, right = st.columns(2)

with left:

    industry_funding = filtered_df.groupby(
        "Industry"
    )["Funding Amount (M USD)"].sum().reset_index()

    fig1 = px.bar(
        industry_funding,
        x="Industry",
        y="Funding Amount (M USD)",
        title="Funding by Industry"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with right:

    fig2 = px.pie(
        filtered_df,
        names="Region",
        title="Startup Distribution by Region"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# -------------------------
# Revenue vs Valuation
# -------------------------

fig3 = px.scatter(
    filtered_df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Employees",
    hover_name="Startup Name",
    title="Revenue vs Valuation Analysis"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# -------------------------
# Startup Growth Trend
# -------------------------

growth = filtered_df.groupby(
    "Year Founded"
).size().reset_index(
    name="Count"
)

fig4 = px.line(
    growth,
    x="Year Founded",
    y="Count",
    markers=True,
    title="Startup Formation Trend"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# -------------------------
# Executive Insights
# -------------------------

st.subheader("📌 Key Insights")

highest_industry = filtered_df.groupby(
    "Industry"
)["Funding Amount (M USD)"].mean().idxmax()

top_region = filtered_df[
    "Region"
].mode()[0]

highest_valuation = filtered_df.loc[
    filtered_df[
        "Valuation (M USD)"
    ].idxmax(),
    "Startup Name"
]

st.success(
    f"Highest funded industry: {highest_industry}"
)

st.info(
    f"Most active region: {top_region}"
)

st.warning(
    f"Highest valuation startup: {highest_valuation}"
)

# -------------------------
# Top Startup Table
# -------------------------

st.subheader("Top 10 Startups")

top10 = filtered_df.sort_values(
    "Valuation (M USD)",
    ascending=False
).head(10)

st.dataframe(
    top10,
    use_container_width=True
)

# -------------------------
# Raw Data Section
# -------------------------

with st.expander("View Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )
