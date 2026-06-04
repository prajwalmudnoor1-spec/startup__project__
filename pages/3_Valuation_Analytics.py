import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------
# Page Configuration
# ------------------------------------

st.set_page_config(
    page_title="Valuation Analytics",
    page_icon="💎",
    layout="wide"
)

# ------------------------------------
# Custom Styling
# ------------------------------------

st.markdown("""
<style>

.main{
background-color:#f7f9fc;
}

h1,h2,h3{
color:#1f4e79;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------
# Load Dataset
# ------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(
        "startup_data.csv"
    )
    return df

df = load_data()

st.title("💎 Valuation Analytics Dashboard")

st.write(
    "Analyze startup valuations and growth patterns"
)

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
# KPI Metrics
# ------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average Valuation",
    f"${filtered_df['Valuation (M USD)'].mean():.2f} M"
)

c2.metric(
    "Highest Valuation",
    f"${filtered_df['Valuation (M USD)'].max():.2f} M"
)

c3.metric(
    "Total Valuation",
    f"${filtered_df['Valuation (M USD)'].sum():.2f} M"
)

c4.metric(
    "Median Valuation",
    f"${filtered_df['Valuation (M USD)'].median():.2f} M"
)

st.divider()

# ------------------------------------
# Valuation Distribution
# ------------------------------------

st.subheader(
    "Valuation Distribution"
)

fig1 = px.histogram(
    filtered_df,
    x="Valuation (M USD)",
    nbins=25,
    title="Distribution of Startup Valuation"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ------------------------------------
# Industry Valuation Comparison
# ------------------------------------

industry_val = filtered_df.groupby(
    "Industry"
)["Valuation (M USD)"].mean().reset_index()

fig2 = px.bar(
    industry_val,
    x="Industry",
    y="Valuation (M USD)",
    title="Average Valuation by Industry"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ------------------------------------
# Revenue vs Valuation
# ------------------------------------

fig3 = px.scatter(
    filtered_df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Employees",
    hover_name="Startup Name",
    title="Revenue vs Valuation"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ------------------------------------
# Year Wise Trend
# ------------------------------------

trend = filtered_df.groupby(
    "Year Founded"
)["Valuation (M USD)"].mean().reset_index()

fig4 = px.line(
    trend,
    x="Year Founded",
    y="Valuation (M USD)",
    markers=True,
    title="Average Valuation Trend"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ------------------------------------
# Top Valued Startups
# ------------------------------------

st.subheader(
    "Top 10 Highest Valued Startups"
)

top = filtered_df.sort_values(
    "Valuation (M USD)",
    ascending=False
).head(10)

st.dataframe(
    top,
    use_container_width=True
)

# ------------------------------------
# Insights Section
# ------------------------------------

st.subheader(
    "Key Insights"
)

best_industry = filtered_df.groupby(
    "Industry"
)["Valuation (M USD)"].mean().idxmax()

highest_company = filtered_df.loc[
    filtered_df[
        "Valuation (M USD)"
    ].idxmax(),
    "Startup Name"
]

st.success(
    f"Highest average valuation industry: {best_industry}"
)

st.info(
    f"Top valued startup: {highest_company}"
)

# ------------------------------------
# Raw Data Viewer
# ------------------------------------

with st.expander(
    "View Dataset"
):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )
