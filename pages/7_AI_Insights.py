import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="AI Insights",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------------
# Styling
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

st.title("🤖 AI Powered Startup Insights")

st.write(
    "Machine learning driven insights and predictive analytics"
)

# -----------------------------------
# Sidebar Filters
# -----------------------------------

st.sidebar.header(
    "AI Filters"
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

# -----------------------------------
# KPI Section
# -----------------------------------

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Companies",
    len(filtered_df)
)

c2.metric(
    "Industries",
    filtered_df["Industry"].nunique()
)

c3.metric(
    "Regions",
    filtered_df["Region"].nunique()
)

c4.metric(
    "Avg Valuation",
    f"${filtered_df['Valuation (M USD)'].mean():.2f}M"
)

st.divider()

# -----------------------------------
# Clustering
# -----------------------------------

st.subheader(
    "Startup Clustering"
)

features = filtered_df[
[
"Funding Amount (M USD)",
"Revenue (M USD)",
"Valuation (M USD)"
]
]

scaler = StandardScaler()

scaled = scaler.fit_transform(
    features
)

model = KMeans(
    n_clusters=4,
    random_state=42
)

filtered_df["Cluster"] = model.fit_predict(
    scaled
)

fig1 = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    color=filtered_df["Cluster"].astype(str),
    hover_name="Startup Name",
    title="AI Startup Segmentation"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# -----------------------------------
# Revenue Prediction
# -----------------------------------

st.subheader(
    "Revenue Forecast"
)

X = filtered_df[
[
"Funding Amount (M USD)",
"Employees"
]
]

y = filtered_df[
    "Revenue (M USD)"
]

reg = LinearRegression()

reg.fit(
    X,
    y
)

future_funding = st.slider(
    "Funding Amount",
    0,
    1000,
    100
)

future_emp = st.slider(
    "Employees",
    1,
    50000,
    1000
)

prediction = reg.predict(
    [[future_funding, future_emp]]
)[0]

st.success(
    f"Predicted Revenue: ${prediction:.2f} M"
)

# -----------------------------------
# Outlier Detection
# -----------------------------------

st.subheader(
    "Unusual Startups"
)

zscore = (
    filtered_df[
        "Valuation (M USD)"
    ]
    -
    filtered_df[
        "Valuation (M USD)"
    ].mean()
) / filtered_df[
    "Valuation (M USD)"
].std()

outliers = filtered_df[
    abs(zscore) > 2
]

st.dataframe(
    outliers,
    use_container_width=True
)

# -----------------------------------
# AI Recommendations
# -----------------------------------

st.subheader(
    "AI Recommendations"
)

best_industry = filtered_df.groupby(
    "Industry"
)["Revenue (M USD)"].mean().idxmax()

best_region = filtered_df.groupby(
    "Region"
)["Valuation (M USD)"].mean().idxmax()

st.info(
    f"High growth industry: {best_industry}"
)

st.success(
    f"Best region for expansion: {best_region}"
)

st.warning(
    "High valuation startups should focus on profitability optimization."
)

# -----------------------------------
# Trend Analytics
# -----------------------------------

trend = filtered_df.groupby(
    "Year Founded"
)["Valuation (M USD)"].mean().reset_index()

fig2 = px.line(
    trend,
    x="Year Founded",
    y="Valuation (M USD)",
    markers=True,
    title="AI Trend Analysis"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -----------------------------------
# Cluster Statistics
# -----------------------------------

cluster_stats = filtered_df.groupby(
    "Cluster"
)[
[
"Funding Amount (M USD)",
"Revenue (M USD)",
"Valuation (M USD)"
]
].mean()

st.subheader(
    "Cluster Statistics"
)

st.dataframe(
    cluster_stats,
    use_container_width=True
)

# -----------------------------------
# Dataset Viewer
# -----------------------------------

with st.expander(
    "View AI Dataset"
):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )
