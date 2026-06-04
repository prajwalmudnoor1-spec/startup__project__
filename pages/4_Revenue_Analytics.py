import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------
# Page Configuration
# ----------------------------------

st.set_page_config(
    page_title="Revenue Analytics",
    page_icon="💰",
    layout="wide"
)

# ----------------------------------
# Custom Styling
# ----------------------------------

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

# ----------------------------------
# Load Dataset
# ----------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "startup_data.csv"
    )

    return df

df = load_data()

st.title("💰 Revenue Analytics Dashboard")

st.write(
    "Analyze startup revenue performance and business growth"
)

# ----------------------------------
# Sidebar Filters
# ----------------------------------

st.sidebar.header(
    "Filters"
)

industry = st.sidebar.multiselect(
    "Industry",
    options=df["Industry"].unique(),
    default=df["Industry"].unique()
)

region = st.sidebar.multiselect(
    "Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry))
    &
    (df["Region"].isin(region))
]

# ----------------------------------
# KPI Metrics
# ----------------------------------

total_revenue = filtered_df[
    "Revenue (M USD)"
].sum()

avg_revenue = filtered_df[
    "Revenue (M USD)"
].mean()

max_revenue = filtered_df[
    "Revenue (M USD)"
].max()

median_revenue = filtered_df[
    "Revenue (M USD)"
].median()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Revenue",
    f"${total_revenue:.2f} M"
)

c2.metric(
    "Average Revenue",
    f"${avg_revenue:.2f} M"
)

c3.metric(
    "Highest Revenue",
    f"${max_revenue:.2f} M"
)

c4.metric(
    "Median Revenue",
    f"${median_revenue:.2f} M"
)

st.divider()

# ----------------------------------
# Revenue Distribution
# ----------------------------------

st.subheader(
    "Revenue Distribution"
)

fig1 = px.histogram(
    filtered_df,
    x="Revenue (M USD)",
    nbins=25,
    title="Revenue Distribution"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ----------------------------------
# Revenue by Industry
# ----------------------------------

industry_rev = filtered_df.groupby(
    "Industry"
)["Revenue (M USD)"].mean().reset_index()

fig2 = px.bar(
    industry_rev,
    x="Industry",
    y="Revenue (M USD)",
    title="Average Revenue by Industry"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ----------------------------------
# Revenue vs Funding
# ----------------------------------

fig3 = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Revenue (M USD)",
    size="Employees",
    color="Industry",
    hover_name="Startup Name",
    title="Funding vs Revenue"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ----------------------------------
# Revenue Growth Trend
# ----------------------------------

trend = filtered_df.groupby(
    "Year Founded"
)["Revenue (M USD)"].mean().reset_index()

fig4 = px.line(
    trend,
    x="Year Founded",
    y="Revenue (M USD)",
    markers=True,
    title="Average Revenue Trend"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ----------------------------------
# Top Revenue Startups
# ----------------------------------

st.subheader(
    "Top 10 Revenue Generating Startups"
)

top_revenue = filtered_df.sort_values(
    "Revenue (M USD)",
    ascending=False
).head(10)

st.dataframe(
    top_revenue,
    use_container_width=True
)

# ----------------------------------
# Insights
# ----------------------------------

st.subheader(
    "Revenue Insights"
)

best_industry = filtered_df.groupby(
    "Industry"
)["Revenue (M USD)"].mean().idxmax()

highest_company = filtered_df.loc[
    filtered_df[
        "Revenue (M USD)"
    ].idxmax(),
    "Startup Name"
]

st.success(
    f"Highest revenue industry: {best_industry}"
)

st.info(
    f"Top revenue startup: {highest_company}"
)

# ----------------------------------
# Dataset Viewer
# ----------------------------------

with st.expander(
    "View Revenue Dataset"
):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )
